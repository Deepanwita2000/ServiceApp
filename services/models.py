from django.db import models
from accountapp.models import User
# Create your models here.
class Service(models.Model):
    #id will be automatically created
    name = models.CharField(max_length=100)
    icon=models.ImageField(upload_to="pics/",blank=True,null=True)
    description = models.TextField()
    admin = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'role': 'admin'}, related_name='services_created')
    
    class Meta:
        unique_together = ['name' , 'admin']

    def __str__(self):
        return self.name



