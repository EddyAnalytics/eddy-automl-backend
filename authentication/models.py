from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    # user reference is not necessary here
    # label is username

    def __str__(self):
        return self.username
