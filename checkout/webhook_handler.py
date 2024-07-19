from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Donation
from profiles.models import UserProfile
import stripe
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, donation):
        """Send the user a confirmation email"""
        cust_email = donation.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'donation': donation})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'donation': donation, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        total = round(stripe_charge.amount / 100, 2)

        profile = None
        username = intent.metadata.username
        profile = UserProfile.objects.get(user__username=username)
        donation_breakdown = intent.metadata.donation_breakdown

        # Create a new donation obj if it doesn't already exist.
        donation_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                donation = Donation.objects.get(
                    stripe_pid=pid,
                    user_profile=profile,
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    total=total,
                )
                # If a match found, the order already exists
                donation_exists = True
                break
            except Donation.DoesNotExist:
                attempt += 1
                # Waits 1 second, before next attempt
                time.sleep(1)
        if donation_exists:
            self._send_confirmation_email(donation)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | SUCCESS: '
                    f'Verified donation already in database'),
                status=200)
        else:
            donation = None
            try:
                # If no match found, after 5 attempts, create the donation obj
                donation = Donation.objects.create(
                    stripe_pid=pid,
                    user_profile=profile,
                    full_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    total=total,
                    dontation_breakdown=donation_breakdown,
                )
            except Exception as e:
                if donation:
                    donation.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        self._send_confirmation_email(donation)
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | SUCCESS: '
                f'Created order in webhook'),
            status=200)

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)
