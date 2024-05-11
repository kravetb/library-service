from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from borrowings_service.models import Borrowing

from datetime import datetime, timedelta

BORROWING_URL = reverse("borrowings-service:borrowing-list")


def sample_bo(**params) -> Borrowing:
    default = {
        "borrow_date": datetime.today(),
        "expected_return_date": datetime.today() + timedelta(days=5),
        "inventory": 5,
        "daily_fee": 1.50,
    }
    default.update(params)
    return Borrowing.objects.create(**default)


class UnauthenticatedBorrowingsApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
