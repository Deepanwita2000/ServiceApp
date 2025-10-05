from django.contrib import admin
from .models import Provider
# Register your models here.
class ProviderDetails(admin.ModelAdmin):
    list_display=[
        'provider',
        'service',
    'experience',
    'chargesPerHour',
    'location',

    ]
admin.site.register(Provider,ProviderDetails)
#     class BookingDetails(admin.ModelAdmin):
#     list_display=[
#         'user',
#         'event',
#         'ticket_tier', 
#         'booked_on',
#         'paymentStatus'
#     ]
# admin.site.register(Booking,BookingDetails)