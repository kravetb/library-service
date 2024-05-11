from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from rest_framework import status

from book_service.models import Book
from book_service.serializers import BookSerializer

BOOK_URL = reverse("book-service:book-list")


def sample_book(**params) -> Book:
    default = {
        "title": "Test",
        "author": "Test Author",
        "inventory": 5,
        "daily_fee": 1.50,
    }
    default.update(params)
    return Book.objects.create(**default)


class UnauthenticatedBookApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_books_list(self):
        sample_book()
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.data, serializer.data)
