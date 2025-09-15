from django.db import models
from services.models import Service
from accountapp.models import User
# Create your models here.
class Catagory(models.Model):
    # id generated automatically
    names = models.JSONField() # ['fan' , 'switch, . 'sockets and wires' ]
    service = models.ForeignKey(Service , on_delete=models.CASCADE , related_name='catagory')
    admin = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'role': 'admin'}, related_name='catagory')
    
    def __str__(self):
        return f"{self.names} - {self.service.name}"
    
    