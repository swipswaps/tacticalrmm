# Generated by Django 3.0.5 on 2020-04-05 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0002_auto_20200405_0706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpuloadcheck',
            name='more_info',
        ),
        migrations.RemoveField(
            model_name='memcheck',
            name='more_info',
        ),
    ]