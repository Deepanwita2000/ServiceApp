from django.urls import include, path
from .views import ProviderRegistrationSet,SearchService,ViewBookings

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('providers', ProviderRegistrationSet)
router.register('public_route', SearchService , basename='public_route')
router.register('ViewBookings', ViewBookings , basename='ViewBookings')
urlpatterns = [
    path('api/', include(router.urls)),

]