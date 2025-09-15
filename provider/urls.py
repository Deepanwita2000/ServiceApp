from django.urls import include, path
from .views import ProviderRegistrationSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('providers', ProviderRegistrationSet)

urlpatterns = [
    path('provider_api/', include(router.urls)),

]