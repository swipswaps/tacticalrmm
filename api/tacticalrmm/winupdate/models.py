import datetime as dt

from django.db import models
from django.contrib.postgres.fields import ArrayField

from agents.models import Agent

PATCH_ACTION_CHOICES = [
    ("inherit", "Inherit"),
    ("approve", "Approve"),
    ("ignore", "Ignore"),
    ("nothing", "Do Nothing"),
]

AUTO_APPROVAL_CHOICES = [
    ("manual", "Manual"),
    ("approve", "Approve"),
    ("ignore", "Ignore"),
    ("inherit", "Inherit"),
]

RUN_TIME_HOUR_CHOICES = [(i, dt.time(i).strftime("%I %p")) for i in range(24)]

RUN_TIME_DAY_CHOICES = [(i + 1, i + 1) for i in range(31)]

REBOOT_AFTER_INSTALL_CHOICES = [
    ("never", "Never"),
    ("required", "When Required"),
    ("always", "Always"),
    ("inherit", "Inherit"),
]

SCHEDULE_FREQUENCY_CHOICES = [
    ("daily", "Daily/Weekly"),
    ("monthly", "Monthly"),
    ("inherit", "Inherit"),
]


class WinUpdate(models.Model):
    agent = models.ForeignKey(
        Agent, related_name="winupdates", on_delete=models.CASCADE
    )
    guid = models.CharField(max_length=255, null=True)
    kb = models.CharField(max_length=100, null=True)
    mandatory = models.BooleanField(default=False)
    title = models.TextField(null=True)
    needs_reboot = models.BooleanField(default=False)
    installed = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)
    description = models.TextField(null=True)
    severity = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(
        max_length=100, choices=PATCH_ACTION_CHOICES, default="nothing"
    )
    result = models.CharField(max_length=255, default="n/a")
    date_installed = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.agent.hostname} {self.kb}"


class WinUpdatePolicy(models.Model):
    agent = models.ForeignKey(
        "agents.Agent",
        related_name="winupdatepolicy",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    policy = models.ForeignKey(
        "automation.Policy",
        related_name="winupdatepolicy",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    critical = models.CharField(
        max_length=100, choices=AUTO_APPROVAL_CHOICES, default="inherit"
    )
    important = models.CharField(
        max_length=100, choices=AUTO_APPROVAL_CHOICES, default="inherit"
    )
    moderate = models.CharField(
        max_length=100, choices=AUTO_APPROVAL_CHOICES, default="inherit"
    )
    low = models.CharField(
        max_length=100, choices=AUTO_APPROVAL_CHOICES, default="inherit"
    )
    other = models.CharField(
        max_length=100, choices=AUTO_APPROVAL_CHOICES, default="inherit"
    )

    run_time_hour = models.IntegerField(choices=RUN_TIME_HOUR_CHOICES, default=3)

    run_time_frequency = models.CharField(
        max_length=100, choices=SCHEDULE_FREQUENCY_CHOICES, default="inherit"
    )

    # 0 to 6 = Monday to Sunday
    run_time_days = ArrayField(
        models.IntegerField(blank=True), null=True, blank=True, default=list
    )

    run_time_day = models.IntegerField(choices=RUN_TIME_DAY_CHOICES, default=1)

    reboot_after_install = models.CharField(
        max_length=50, choices=REBOOT_AFTER_INSTALL_CHOICES, default="inherit"
    )

    reprocess_failed_inherit = models.BooleanField(default=True)
    reprocess_failed = models.BooleanField(default=False)
    reprocess_failed_times = models.PositiveIntegerField(default=5)
    email_if_fail = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    modified_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        if self.agent:
            return self.agent.hostname
        else:
            return self.policy.name

    @staticmethod
    def serialize(policy):
        # serializes the policy and returns json
        from .serializers import WinUpdatePolicySerializer

        return WinUpdatePolicySerializer(policy).data
