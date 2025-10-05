from django.db import models
from services.models import Service
from accountapp.models import User
# Create your models here.
class Catagory(models.Model):
    # id generated automatically
    name=models.CharField() # switch ans socket , Fan , 
    description = models.TextField() #service overiew
    image= models.ImageField(upload_to="catagory/",blank=True,null=True)
    service = models.ForeignKey(Service , on_delete=models.CASCADE , related_name='catagory')
    facilities = models.JSONField() # ['fan' , 'switch, . 'sockets and wires' ]
    price = models.DecimalField(max_digits=5, decimal_places=2)
    admin = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'role': 'admin'}, related_name='catagory')
    
    def __str__(self):
        return f"{self.name} - {self.service.name}"
    
    