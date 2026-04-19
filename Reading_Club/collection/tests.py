from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from Reading_Club.author.models import Author
from Reading_Club.book.models import Book
from Reading_Club.collection.models import Collection

User = get_user_model()
PASSWORD = 'TestPass123!'


def make_user(username='coluser', nickname='CU'):
    return User.objects.create_user(username=username, nickname=nickname, password=PASSWORD)


def make_book(name='Col Book'):
    author = Author.objects.create(publishing_name=f'Author of {name}')
    return Book.objects.create(name=name, author=author, genre='drama')


def make_collection(title='My Collection', user=None):
    col = Collection.objects.create(title=title, created_by=user, description='A test collection')
    return col


class CollectionModelTest(TestCase):

    def setUp(self):
        self.user = make_user()

    def test_slug_generated_from_title(self):
        col = make_collection(title='Best Sci-Fi', user=self.user)
        self.assertEqual(col.collection_slug, 'best-sci-fi')

    def test_str_returns_title(self):
        col = make_collection(title='My Picks', user=self.user)
        self.assertEqual(str(col), 'My Picks')


class CollectionListDetailTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.collection = make_collection(user=self.user)

    def test_collection_list_loads(self):
        response = self.client.get(reverse('collections:list'))
        self.assertEqual(response.status_code, 200)

    def test_collection_detail_loads(self):
        response = self.client.get(
            reverse('collections:details', kwargs={'slug': self.collection.collection_slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.collection.title)


class CollectionCreateTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.book = make_book()

    def test_create_requires_login(self):
        response = self.client.get(reverse('collections:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_logged_in_user_can_create_collection(self):
        self.client.force_login(self.user)
        self.client.post(reverse('collections:create'), {
            'title': 'New Collection',
            'description': 'Some books',
            'books': [self.book.pk],
        })
        self.assertTrue(Collection.objects.filter(title='New Collection').exists())

    def test_create_sets_created_by(self):
        self.client.force_login(self.user)
        self.client.post(reverse('collections:create'), {
            'title': 'Owned Collection',
            'description': 'Mine',
            'books': [self.book.pk],
        })
        col = Collection.objects.get(title='Owned Collection')
        self.assertEqual(col.created_by, self.user)


class CollectionEditDeleteTest(TestCase):

    def setUp(self):
        self.owner = make_user(username='col_owner', nickname='CO')
        self.other = make_user(username='col_other', nickname='OT')
        self.book = make_book()
        self.collection = make_collection(title='Editable', user=self.owner)
        self.collection.books.add(self.book)

    def test_owner_can_edit_collection(self):
        self.client.force_login(self.owner)
        self.client.post(
            reverse('collections:edit', kwargs={'slug': self.collection.collection_slug}),
            {'title': 'Renamed', 'description': 'Updated', 'books': [self.book.pk]}
        )
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.title, 'Renamed')

    def test_non_owner_gets_403_on_edit(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse('collections:edit', kwargs={'slug': self.collection.collection_slug}),
            {'title': 'Hijacked', 'description': 'No', 'books': [self.book.pk]}
        )
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_collection(self):
        self.client.force_login(self.owner)
        self.client.post(
            reverse('collections:delete', kwargs={'slug': self.collection.collection_slug})
        )
        self.assertFalse(Collection.objects.filter(pk=self.collection.pk).exists())

    def test_non_owner_gets_403_on_delete(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse('collections:delete', kwargs={'slug': self.collection.collection_slug})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Collection.objects.filter(pk=self.collection.pk).exists())