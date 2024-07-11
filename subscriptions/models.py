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


class Donation(models.Model):
    donation_number = models.CharField(
        max_length=32, null=False, editable=False, default=0
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
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

    def _send_donation_changed_email(self):
        """
        Send the user notification of a upcoming donation change via email
        """
        cust_email = self.user.email
        subject = render_to_string(
            'subscriptions/confirmation_emails/'
            'donation-changed-subject.txt',
            {'donation': self}
        )
        body = render_to_string(
            'subscriptions/confirmation_emails/'
            'donation-changed-body.txt',
            {
                'donation': self,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            }
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )
