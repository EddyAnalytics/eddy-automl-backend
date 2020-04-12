
from django.db import models


# Create your models here.
from authentication.models import User


class AutoMLJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_topic = models.CharField(max_length=100)
    output_topic = models.CharField(max_length=100)
    target_column = models.CharField(max_length=100)

    @classmethod
    def create(cls, user, input_topic, output_topic, target_column):
        job = cls(user=user,
                  input_topic=input_topic,
                  output_topic=output_topic,
                  target_column=target_column)
        return job
