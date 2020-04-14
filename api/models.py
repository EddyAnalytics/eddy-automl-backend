from enum import Enum

from django.db import models

# Create your models here.
from authentication.models import User


class JobStatus(Enum):
    RUNNING = 0
    STOPPED = 1

    FAILED = -1

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class AutoMLJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_topic = models.CharField(max_length=100)
    output_topic = models.CharField(max_length=100)
    target_column = models.CharField(max_length=100)

    name = models.CharField(max_length=100)

    status = models.IntegerField(choices=JobStatus.choices())

    @classmethod
    def create(cls, user, input_topic, output_topic, target_column, name, status):
        job = cls(user=user,
                  input_topic=input_topic,
                  output_topic=output_topic,
                  target_column=target_column,
                  name=name,
                  status=status
        )
        return job


