# Generated by Django 2.2.10 on 2020-04-15 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200414_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automljob',
            name='target_column',
            field=models.IntegerField(max_length=100),
        ),
    ]
