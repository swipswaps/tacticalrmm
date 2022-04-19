# Generated by Django 3.0.6 on 2020-06-04 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agents", "0003_agent_checks_last_generated"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="checks_last_generated",
        ),
        migrations.AddField(
            model_name="agent",
            name="policies_pending",
            field=models.BooleanField(default=False),
        ),
    ]
