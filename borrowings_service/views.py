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
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create-borrowing":
            return BorrowingCreateSerializer

        return BorrowingListSerializer

    @action(
        methods=["POST"],
        detail=False,
        url_path="create-borrowing",
        permission_classes=[],
    )
    def create_borrowing(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)
        if serializer.is_valid():
            book.inventory -= 1
            book.save()
            print(request.data)
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
