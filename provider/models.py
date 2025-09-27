from django.db import models
from services.models import Service

from accountapp.models import User
# Create your models here.
class Provider(models.Model):
    #id will be auto generated
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='providers' , limit_choices_to={'role':'provider'})  # Link to User(role=provider)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='providers')    # Link to service
    pincode = models.BigIntegerField(null=False)  # List of zip codes where the service is available
    experience = models.IntegerField(null=False)     # Years of experience of the provider
    chargesPerHour = models.DecimalField(max_digits=5, decimal_places=2)  # Charges per hour
    image=models.ImageField(upload_to="provider/",blank=True,null=True)
    location = models.CharField()   
    # is_available = models.BooleanField(default=True)  # Availability status
    is_approved = models.BooleanField(default=False , null=False)
    
    def __str__(self):
        return f"{self.service.name}-{self.provider.email}"

    