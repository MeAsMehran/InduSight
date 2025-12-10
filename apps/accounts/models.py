from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(region="IR", unique=True)
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return str(self.phone_number)


class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES,)

    def __str__(self):
        return self.get_name_display()
