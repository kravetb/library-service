from rest_framework import routers
from borrowings_service.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)

urlpatterns = router.urls

app_name = "borrowings_service"
