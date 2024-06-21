from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager

AUTH_PROVIDERS = {"email": "email"}

class Role(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    otp = models.CharField(max_length=6, null=True, blank=True)
    roles = models.ManyToManyField(Role)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return self.email
