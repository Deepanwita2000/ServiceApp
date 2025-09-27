from django.urls import include, path
from .views import UserBookingViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('customer', UserBookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

]