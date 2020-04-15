from django.db import models

# Create your models here.
from authentication.models import User
from k8s.util import JobStatus


class AutoMLJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_topic = models.CharField(max_length=100)
    output_topic = models.CharField(max_length=100)
    target_column = models.IntegerField()

    job_name = models.CharField(max_length=100)
    pod_name = models.CharField(max_length=100, blank=True, null=True)

    status = models.IntegerField(choices=JobStatus.choices())



