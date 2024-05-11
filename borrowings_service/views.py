from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from book_service.models import Book
from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user", "book")
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        is_active = self.request.query_params.get("is_active")
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id", None)
        if user.is_superuser or user.is_staff:
            if user_id:
                queryset = queryset.filter(user=user_id)

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        if user.is_superuser or user.is_staff:
            return queryset

        return queryset.filter(user=user)

    def get_serializer_class(self):

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingListSerializer

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="return-borrowing",
        permission_classes=[IsAuthenticated, ],
    )
    def return_borrowing(self, request, pk=None):

        try:
            borrowing = Borrowing.objects.get(pk=pk)
        except Borrowing.DoesNotExist:
            raise exceptions.NotFound("Borrowing with this ID does not exist.")

        serializer = BorrowingReturnSerializer(borrowing, data=request.data, partial=True)

        if serializer.is_valid():
            book = borrowing.book
            book.inventory += 1
            book.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        detail=False,
        url_path="create-borrowing",
        permission_classes=[IsAuthenticated, ],
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
