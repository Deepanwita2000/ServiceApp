# from django.urls import path
# from . import views

# urlpatterns=[


#     # API Routes
#     path("api_add_catagory/",views.api_add_catagory,name="api_add_catagory"),
#     path("api_view_catagory/",views.api_view_catagory,name="api_view_catagory"),
#     # path('api_update_subject/<int:pk>/', views.api_update_subject, name='api_update_subject'),
#     # path('api_delete_subject/<int:pk>/', views.api_delete_subject, name='api_delete_subject'),
    
# ]

from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter
from .views import CatagoryViewSet

router = DefaultRouter()
router.register('lists', CatagoryViewSet)

urlpatterns = [
    # for api
    # path('api_add_service/',views.api_add_service , name='api_add_service'),
    # path('api_view_service/',views.api_view_service , name='api_view_service'),
    # path('api_edit_service/<int:pk>/',views.api_edit_service , name='api_edit_service'),
    # path('api_delete_service/<int:service_id>/',views.api_delete_service , name='api_delete_service'),

    # for admin
    # path('view_service/',views.view_service , name='view_service'),
    # path('add_service/',views.add_service , name='add_service'),
    # path('edit_service/<int:pk>/',views.edit_service , name='edit_service'),
    # path('delete_service/<int:service_id>/',views.delete_service , name='delete_service'),

    # for api-> CBV
    path('api_catagory/', include(router.urls)),

]
