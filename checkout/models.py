import uuid
from django.db import models
from django.conf import settings


class Donation(models.Model):
    donation_number = models.CharField(
        max_length=32, null=False, editable=False, default=0
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    donation_breakdown = models.JSONField(default=dict, blank=False)
    date = models.DateField(auto_now_add=True)

    def _generate_donation_number(self):
        """
        Generate a random, unique donation number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        If the Donation uuid hasn't been set already,
        override save to set it first
        """
        if not self.donation_number:
            self.donation_number = self._generate_donation_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.donation_number

# ADD A SEND CONFIRMATION OF DONATION EMAIL HERE
