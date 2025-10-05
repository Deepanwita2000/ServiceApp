from django.contrib import admin
from .models import Rating
# Register your models here.
class RatingDetails(admin.ModelAdmin):
    list_display=[
       'booking',
        'provider',
        'user',
        'stars',
        'comment',
        'rated_at'

    ]
admin.site.register(Rating,RatingDetails)