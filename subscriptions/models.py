import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Subscription(models.Model):
    """
    Subscription model to hold the user's current subscription settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sub_active = models.BooleanField(default=True)
    sub_total = models.PositiveIntegerField(default=0, null=False)
    sub_breakdown = models.JSONField(default=dict, blank=True)
