from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    code = models.CharField(max_length=6, blank=True, null=True)
    code_created_at = models.DateTimeField(blank=True, null=True)
