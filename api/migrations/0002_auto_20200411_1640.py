# Generated by Django 2.2.10 on 2020-04-11 16:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ML_job',
            new_name='AutoMLJob',
        ),
    ]
