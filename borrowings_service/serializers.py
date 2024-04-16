from rest_framework import serializers
from borrowings_service.models import Borrowing

from book_service.serializers import BookSerializer


class BorrowingListSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    book_author = serializers.CharField(source="book.author", read_only=True)
    book_inventory = serializers.IntegerField(source="book.inventory", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "book_author",
            "book_inventory"
        )
