from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from book_service.models import Book
from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer, BorrowingCreateSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user", "book")

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Borrowing.objects.all()

        return Borrowing.objects.filter(user=user)

    def get_serializer_class(self):

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingListSerializer

    @action(
        methods=["POST"],
        detail=False,
        url_path="create-borrowing",
        permission_classes=[],
    )
    def create_borrowing(self, request):
        serializer = BorrowingCreateSerializer(data=request.data)
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)
        if serializer.is_valid():
            book.inventory -= 1
            book.save()
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
