from django.db import models
from library_service.settings import AUTH_USER_MODEL
from book_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True, null=False, blank=False)
    expected_return_date = models.DateField(null=False, blank=False)
    actual_return_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings_service")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings_service")

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"
