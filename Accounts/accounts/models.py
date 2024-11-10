from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    profile_img = models.URLField()
    social_id = models.CharField(max_length=200, unique=True)
    created_date = models.DateField(auto_now_add=True)