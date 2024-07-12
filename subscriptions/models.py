from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    """
    Subscription model to hold the user's current subscription settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sub_active = models.BooleanField(default=True)
    sub_total = models.PositiveIntegerField(default=0, null=False)
    sub_breakdown = models.JSONField(default=dict, blank=True)
