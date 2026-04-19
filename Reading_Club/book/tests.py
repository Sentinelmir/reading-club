from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from Reading_Club.author.models import Author
from Reading_Club.book.models import Book
from Reading_Club.review.models import Review

User = get_user_model()
PASSWORD = 'TestPass123!'


def make_user(username='bookuser', nickname='BU'):
    return User.objects.create_user(username=username, nickname=nickname, password=PASSWORD)


def make_author(name='Test Author'):
    return Author.objects.create(publishing_name=name)


def make_book(name='Test Book', genre='drama', user=None):
    author = make_author(f'Author of {name}')
    return Book.objects.create(name=name, author=author, genre=genre, created_by=user)


class BookModelTest(TestCase):

    def test_slug_generated_from_name(self):
        book = make_book(name='The Great Gatsby')
        self.assertEqual(book.book_slug, 'the-great-gatsby')

    def test_slug_not_changed_on_resave(self):
        book = make_book(name='Original')
        slug_before = book.book_slug
        book.description = 'Changed'
        book.save()
        self.assertEqual(book.book_slug, slug_before)

    def test_str_returns_book_name(self):
        book = make_book(name='Dune')
        self.assertEqual(str(book), 'Dune')

    def test_average_rating_is_none_with_no_reviews(self):
        book = make_book()
        self.assertIsNone(book.average_rating)

    def test_average_rating_calculated_from_reviews(self):
        user = make_user()
        book = make_book()
        Review.objects.create(book=book, author=user, text='Good', rating=4)
        Review.objects.create(book=book, author=user, text='OK', rating=2)
        self.assertEqual(book.average_rating, 3.0)


class BookListViewTest(TestCase):

    def setUp(self):
        make_book(name='Fantasy Book', genre='fantasy')
        make_book(name='Drama Book', genre='drama')

    def test_list_page_loads(self):
        response = self.client.get(reverse('books:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_shows_all_books(self):
        response = self.client.get(reverse('books:list'))
        self.assertEqual(len(response.context['books']), 2)

    def test_filter_by_genre_returns_correct_books(self):
        response = self.client.get(reverse('books:list') + '?genre=fantasy')
        self.assertEqual(len(response.context['books']), 1)
        self.assertEqual(response.context['books'][0].name, 'Fantasy Book')

    def test_search_by_title(self):
        response = self.client.get(reverse('books:list') + '?search=Drama')
        self.assertEqual(len(response.context['books']), 1)
        self.assertEqual(response.context['books'][0].name, 'Drama Book')

    def test_search_with_no_match_returns_empty(self):
        response = self.client.get(reverse('books:list') + '?search=zzznomatch')
        self.assertEqual(len(response.context['books']), 0)


class BookDetailViewTest(TestCase):

    def setUp(self):
        self.book = make_book(name='Detail Book')

    def test_detail_page_loads(self):
        response = self.client.get(
            reverse('books:details', kwargs={'slug': self.book.book_slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Book')

    def test_detail_returns_404_for_missing_book(self):
        response = self.client.get(
            reverse('books:details', kwargs={'slug': 'does-not-exist'})
        )
        self.assertEqual(response.status_code, 404)


class BookCreateViewTest(TestCase):

    def setUp(self):
        self.user = make_user()

    def test_add_book_page_requires_login(self):
        response = self.client.get(reverse('books:add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_logged_in_user_can_add_book(self):
        self.client.force_login(self.user)
        self.client.post(reverse('books:add'), {
            'name': 'New Book',
            'author_name': 'New Author',
            'genre': 'mystery',
        })
        self.assertTrue(Book.objects.filter(name='New Book').exists())

    def test_add_book_sets_created_by_to_current_user(self):
        self.client.force_login(self.user)
        self.client.post(reverse('books:add'), {
            'name': 'My Book',
            'author_name': 'Some Author',
            'genre': 'drama',
        })
        book = Book.objects.get(name='My Book')
        self.assertEqual(book.created_by, self.user)

    def test_add_book_creates_new_author_if_not_exists(self):
        self.client.force_login(self.user)
        self.client.post(reverse('books:add'), {
            'name': 'Book With New Author',
            'author_name': 'Brand New Author',
            'genre': 'drama',
        })
        self.assertTrue(Author.objects.filter(publishing_name='Brand New Author').exists())

    def test_add_book_reuses_existing_author(self):
        Author.objects.create(publishing_name='Existing Author')
        self.client.force_login(self.user)
        self.client.post(reverse('books:add'), {
            'name': 'Another Book',
            'author_name': 'Existing Author',
            'genre': 'drama',
        })
        self.assertEqual(Author.objects.filter(publishing_name='Existing Author').count(), 1)


class BookDeleteViewTest(TestCase):

    def setUp(self):
        self.owner = make_user(username='owner', nickname='Owner')
        self.other = make_user(username='other', nickname='Other')
        self.book = make_book(name='Owned Book', user=self.owner)

    def test_owner_can_delete_book(self):
        self.client.force_login(self.owner)
        self.client.post(reverse('books:delete', kwargs={'slug': self.book.book_slug}))
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_non_owner_gets_403_on_delete(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse('books:delete', kwargs={'slug': self.book.book_slug})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

    def test_delete_requires_login(self):
        response = self.client.post(
            reverse('books:delete', kwargs={'slug': self.book.book_slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)