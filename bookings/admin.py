from django.contrib import admin

# Register your models here.
from .models import Booking
# Register your models here.
class BookingDetails(admin.ModelAdmin):
    list_display=[
        'customer',
        'service',
        'catagory',
        'pincode',
        'status',
        'booked_at'
    ]
admin.site.register(Booking,BookingDetails)