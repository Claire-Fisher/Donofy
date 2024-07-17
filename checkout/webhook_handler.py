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
        email = donation.email
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
            [email]
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
        metadata = intent.metadata
        donation_data = {
            "full_name": metadata.get('full_name'),
            "email": metadata.get('email'),
            "phone_number": metadata.get('phone_number'),
            "country": metadata.get('country'),
            "postcode": metadata.get('postcode'),
            "town_or_city": metadata.get('town_or_city'),
            "street_address1": metadata.get('street_address1'),
            "street_address2": metadata.get('street_address2'),
            "county": metadata.get('county'),
            "total": metadata.get('total'),
        }

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        intent.total = round(stripe_charge.amount / 100, 2)

        # Clean up shipping details, of which there are none. 
        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        profile = None
        username = intent.metadata.username
        profile = UserProfile.objects.get(user__username=username)

        # Create a new donation obj if it doesn't already exist.
        donation_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                donation = Donation.objects.get(
                    user_profile=profile,
                    full_name__iexact=donation_data['full_name'],
                    email__iexact=donation_data['email'],
                    phone_number__iexact=donation_data['phone_number'],
                    country__iexact=donation_data['country'],
                    postcode__iexact=donation_data['postcode'],
                    town_or_city__iexact=donation_data['town_or_city'],
                    street_address1__iexact=donation_data['street_address1'],
                    street_address2__iexact=donation_data['street_address2'],
                    county__iexact=donation_data['county'],
                    total=donation_data['total'],
                    stripe_pid=pid,
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
                    user_profile=profile,
                    full_name=donation_data['full_name'],
                    email=donation_data['email'],
                    phone_number=donation_data['phone_number'],
                    country=donation_data['country'],
                    postcode=donation_data['postcode'],
                    town_or_city=donation_data['town_or_city'],
                    street_address1=donation_data['street_address1'],
                    street_address2=donation_data['street_address2'],
                    county=donation_data['county'],
                    total=donation_data['total'],
                    stripe_pid=pid,
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
