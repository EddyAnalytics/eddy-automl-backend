from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ML_job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_topic = models.CharField(max_length=100)
    output_topic = models.CharField(max_length=100)
    target_column = models.CharField(max_length=100)
