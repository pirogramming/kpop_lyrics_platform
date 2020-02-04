from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.models import UserManager as DefaultUserManager


class User(AbstractUser):
    alias = models.CharField(max_length=255, unique=True, verbose_name='닉네임')
    interest = models.CharField(max_length=255, blank=True, verbose_name='관심사')



UserManager