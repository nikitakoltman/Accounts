# Generated by Django 3.0.8 on 2020-09-26 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_profile_training_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='training_completed',
        ),
    ]
