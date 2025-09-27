from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import views,settings
urlpatterns = [
    path('admin/', admin.site.urls),

    # for homr page
    path('',views.home , name='home'),

    path('service/',include('services.urls')),
    path('catagory/',include('catagory.urls')),
    path('provider/',include('provider.urls')),
    path('accountapp/',include('accountapp.urls')),
    path('bookings/',include('bookings.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)