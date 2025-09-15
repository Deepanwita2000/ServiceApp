from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Role constants
    ADMIN = 'admin'
    Customer = 'customer'
    Provider = 'provider'

     # Role choices
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (Customer, 'Customer'),
        (Provider, 'Provider'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
   
    email = models.EmailField(unique=True)
    #password
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #profile image
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email 


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email} (Expires: {self.expired_at})"


