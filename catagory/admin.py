from django.contrib import admin

# Register your models here.
from .models import Catagory
# Register your models here.
class CategoryDetails(admin.ModelAdmin):
    list_display=[
            'name',
            'image',
            'service',
            'price'
    
            ]
admin.site.register(Catagory,CategoryDetails)