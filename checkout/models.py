import uuid
from django.db import models
from django.conf import settings
from profiles.models import UserProfile
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.validators import RegexValidator, EmailValidator


class Donation(models.Model):
    donation_number = models.CharField(
        max_length=32, null=False, editable=False, unique=True
    )
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, unique=True
    )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='donations'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")],
        max_length=254,
        null=False,
        blank=False
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
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
        return f"Donation {self.id} by {self.full_name}"


@receiver(post_save, sender=Donation)
def send_confirmation_email(sender, instance, created, **kwargs):
    """Send the user a confirmation email"""
    if created:
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'donation': instance})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'donation': instance,
                'contact_email': settings.DEFAULT_FROM_EMAIL})
        recipient = [instance.email]
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            recipient,
        )
