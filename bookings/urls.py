from django.urls import include, path
from .views import UserBookingViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('bookings_service', UserBookingViewSet)

urlpatterns = [
    path('book_api/', include(router.urls)),

]