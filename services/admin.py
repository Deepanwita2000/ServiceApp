from django.contrib import admin

from .models import Service
# Register your models here.
class ServiceDetails(admin.ModelAdmin):
    list_display=[
                    'name',
                    'icon',
                    'description'
                        
            ]
admin.site.register(Service,ServiceDetails)