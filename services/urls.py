from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet

router = DefaultRouter()
router.register('services', ServiceViewSet)

urlpatterns = [
    # for api
    # path('api_add_service/',views.api_add_service , name='api_add_service'),
    # path('api_view_service/',views.api_view_service , name='api_view_service'),
    # path('api_edit_service/<int:pk>/',views.api_edit_service , name='api_edit_service'),
    # path('api_delete_service/<int:service_id>/',views.api_delete_service , name='api_delete_service'),

    # for admin
    path('view_service/',views.view_service , name='view_service'),
    path('add_service/',views.add_service , name='add_service'),
    path('edit_service/<int:pk>/',views.edit_service , name='edit_service'),
    path('delete_service/<int:service_id>/',views.delete_service , name='delete_service'),

    # for api-> CBV
    path('api/', include(router.urls)),

]


