from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from Reading_Club.author.models import Author
from Reading_Club.book.models import Book
from Reading_Club.review.models import Review

User = get_user_model()
PASSWORD = 'TestPass123!'


def make_user(username='reviewer', nickname='RV'):
    return User.objects.create_user(username=username, nickname=nickname, password=PASSWORD)


def make_book(name='Review Book'):
    author = Author.objects.create(publishing_name=f'Author of {name}')
    return Book.objects.create(name=name, author=author, genre='drama')


class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.book = make_book()

    def test_str_contains_book_name_and_rating(self):
        review = Review.objects.create(book=self.book, author=self.user, text='Nice', rating=4)
        self.assertIn(self.book.name, str(review))
        self.assertIn('4/5', str(review))

    def test_str_shows_anonymous_when_no_author(self):
        review = Review.objects.create(book=self.book, author=None, text='Ok', rating=3)
        self.assertIn('Anonymous', str(review))

    def test_date_is_set_automatically_on_create(self):
        review = Review.objects.create(book=self.book, author=self.user, text='Auto', rating=5)
        self.assertIsNotNone(review.date_of_publication)


class ReviewCreateTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.book = make_book()

    def test_logged_in_user_can_post_review(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('reviews:create', kwargs={'slug': self.book.book_slug}),
            {'text': 'Great book!', 'rating': 5}
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().author, self.user)

    def test_anonymous_user_can_post_review(self):
        self.client.post(
            reverse('reviews:create', kwargs={'slug': self.book.book_slug}),
            {'text': 'Anonymous opinion', 'rating': 3}
        )
        review = Review.objects.first()
        self.assertIsNotNone(review)
        self.assertIsNone(review.author)

    def test_create_redirects_to_book_detail(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('reviews:create', kwargs={'slug': self.book.book_slug}),
            {'text': 'Good', 'rating': 4}
        )
        self.assertRedirects(
            response,
            reverse('books:details', kwargs={'slug': self.book.book_slug})
        )

    def test_missing_text_does_not_save_review(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('reviews:create', kwargs={'slug': self.book.book_slug}),
            {'text': '', 'rating': 4}
        )
        self.assertEqual(Review.objects.count(), 0)


class ReviewEditTest(TestCase):

    def setUp(self):
        self.owner = make_user(username='owner', nickname='O')
        self.other = make_user(username='other', nickname='OT')
        self.book = make_book()
        self.review = Review.objects.create(
            book=self.book, author=self.owner, text='Original', rating=3
        )

    def test_owner_can_edit_review(self):
        self.client.force_login(self.owner)
        self.client.post(
            reverse('reviews:edit', kwargs={'pk': self.review.pk}),
            {'text': 'Updated', 'rating': 5}
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.text, 'Updated')

    def test_non_owner_gets_403_on_edit(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse('reviews:edit', kwargs={'pk': self.review.pk}),
            {'text': 'Hacked', 'rating': 1}
        )
        self.assertEqual(response.status_code, 403)
        self.review.refresh_from_db()
        self.assertEqual(self.review.text, 'Original')


class ReviewDeleteTest(TestCase):

    def setUp(self):
        self.owner = make_user(username='del_owner', nickname='DO')
        self.other = make_user(username='del_other', nickname='DOT')
        self.book = make_book()
        self.review = Review.objects.create(
            book=self.book, author=self.owner, text='To delete', rating=4
        )

    def test_owner_can_delete_review(self):
        self.client.force_login(self.owner)
        self.client.post(reverse('reviews:delete', kwargs={'pk': self.review.pk}))
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_non_owner_gets_403_on_delete(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse('reviews:delete', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())


class ReviewListTest(TestCase):

    def test_review_list_page_loads(self):
        response = self.client.get(reverse('reviews:list'))
        self.assertEqual(response.status_code, 200)