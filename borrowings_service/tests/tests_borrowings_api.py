from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from borrowings_service.models import Borrowing

from datetime import datetime, timedelta

from book_service.tests.tests_book_api import sample_book
from borrowings_service.serializers import BorrowingListSerializer, BorrowingDetailSerializer

BORROWING_URL = reverse("borrowings-service:borrowing-list")


def sample_borrowing(**params) -> Borrowing:
    default = {
        "borrow_date": datetime.today(),
        "expected_return_date": datetime.today() + timedelta(days=5),
        "actual_return_date": None,
        "book": None,
        "user": None,
    }
    default.update(params)
    return Borrowing.objects.create(**default)


class UnauthenticatedBorrowingsApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            password="testpassword"
        )
        self.test_superuser = get_user_model().objects.create_superuser(
            email="test@seconduser.com",
            password="secondpassword"
        )
        self.book = sample_book()
        self.borrowing = sample_borrowing(book=self.book, user=self.user)
        self.second_borrowing = sample_borrowing(book=self.book, user=self.test_superuser)
        self.borrowing_with_actual_return_date = sample_borrowing(
            book=self.book, user=self.user, actual_return_date="2024-05-20"
        )

    def test_borrowings_list(self):
        self.client.force_authenticate(self.user)
        res = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.filter(user=self.user.id)
        serializer = BorrowingListSerializer(borrowings, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_borrowings_detail(self):
        self.client.force_authenticate(self.user)
        url = reverse("borrowings-service:borrowing-detail", args=[self.borrowing.id])
        res = self.client.get(url)
        borrowing = Borrowing.objects.get(id=self.borrowing.id)
        serializer = BorrowingDetailSerializer(borrowing, many=False)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_list_by_superuser(self):
        self.client.force_authenticate(self.test_superuser)
        res = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_filtering_for_super_user_bu_user_id(self):
        self.client.force_authenticate(self.test_superuser)
        url = f"{BORROWING_URL}?user_id={self.user.id}"
        res = self.client.get(url)
        borrowings = Borrowing.objects.filter(user=self.user.id)
        serializer = BorrowingListSerializer(borrowings, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_filtering_by_is_active(self):
        self.client.force_authenticate(self.user)
        is_active = True
        url = f"{BORROWING_URL}?is_active={is_active}"
        res = self.client.get(url)
        borrowings = Borrowing.objects.filter(actual_return_date__isnull=True)
        serializer = BorrowingListSerializer(borrowings, many=True)
        self.assertEqual(res.data, serializer.data)

