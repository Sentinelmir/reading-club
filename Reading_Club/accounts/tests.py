from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
PASSWORD = 'TestPass123!'


def make_user(username='testuser', nickname='Tester'):
    return User.objects.create_user(username=username, nickname=nickname, password=PASSWORD)


class RegistrationTest(TestCase):

    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'nickname': 'Nick',
            'email': 'new@example.com',
            'password1': PASSWORD,
            'password2': PASSWORD,
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_without_nickname_fails(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'nonickname',
            'nickname': '',
            'password1': PASSWORD,
            'password2': PASSWORD,
        })
        self.assertFalse(User.objects.filter(username='nonickname').exists())
        self.assertFormError(response.context['form'], 'nickname', 'This field is required.')

    def test_register_assigns_readers_group(self):
        self.client.post(reverse('accounts:register'), {
            'username': 'groupuser',
            'nickname': 'GU',
            'email': 'g@example.com',
            'password1': PASSWORD,
            'password2': PASSWORD,
        })
        user = User.objects.get(username='groupuser')
        self.assertTrue(user.groups.filter(name='Readers').exists())

    def test_duplicate_username_is_rejected(self):
        make_user(username='taken')
        self.client.post(reverse('accounts:register'), {
            'username': 'taken',
            'nickname': 'Other',
            'password1': PASSWORD,
            'password2': PASSWORD,
        })
        self.assertEqual(User.objects.filter(username='taken').count(), 1)


class LoginLogoutTest(TestCase):

    def setUp(self):
        self.user = make_user()

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_valid_login_redirects_to_profile(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': PASSWORD,
        })
        self.assertRedirects(response, reverse('accounts:details'))

    def test_wrong_password_does_not_log_in(self):
        self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        response = self.client.get(reverse('accounts:details'))
        self.assertEqual(response.status_code, 302)  # still redirected to login

    def test_logout_redirects_to_homepage(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('homepage'))


class ProfileTest(TestCase):

    def setUp(self):
        self.user = make_user()

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse('accounts:details'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_profile_page_loads_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:details'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.nickname)

    def test_public_profile_loads_for_existing_user(self):
        response = self.client.get(
            reverse('accounts:public_profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_public_profile_returns_404_for_unknown_user(self):
        response = self.client.get(
            reverse('accounts:public_profile', kwargs={'username': 'nobody'})
        )
        self.assertEqual(response.status_code, 404)

    def test_edit_profile_requires_login(self):
        response = self.client.get(reverse('accounts:edit'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_edit_profile_saves_bio(self):
        self.client.force_login(self.user)
        self.client.post(reverse('accounts:edit'), {
            'username': self.user.username,
            'nickname': self.user.nickname,
            'email': 'test@example.com',
            'bio': 'I love reading.',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'I love reading.')

    def test_username_cannot_be_changed_via_edit_form(self):
        self.client.force_login(self.user)
        original_username = self.user.username
        self.client.post(reverse('accounts:edit'), {
            'username': 'hacked_name',
            'nickname': self.user.nickname,
            'email': 'test@example.com',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, original_username)