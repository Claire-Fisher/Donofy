from django.db import models
from djano.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class subscription(models.Model):
    """
    Subscription model to hold the user's current subscription settings. 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sub_active = models.BooleanField(default=False)
    sub_total = models.PositiveIntegerField(default=0, null=False)
    sub_breakdown = models.JSONField(defaul=dict)
