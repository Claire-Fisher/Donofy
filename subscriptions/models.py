import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Subscription(models.Model):
    """
    Subscription model to hold the user's current subscription settings. 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sub_active = models.BooleanField(default=False)
    sub_total = models.PositiveIntegerField(default=0, null=False)
    sub_breakdown = models.JSONField(default=dict, blank=True)


class Donation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_breakdown = models.JSONField(default=dict, blank=False)
    date = models.DateField(auto_now_add=True)

    def _generate_donation_number(self):
        """
        Generate a random, unique donation number using UUID
        """
        return uuid.uuid4().hex.upper()
