from rest_framework import viewsets
from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingListSerializer
