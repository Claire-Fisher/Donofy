from django.http import HttpResponse
from .models import Donation
from profiles.models import UserProfile, Subscription
import stripe
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

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

        try:
            stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        except Exception as e:
            return HttpResponse(
                content=f"Error retrieving charge: {e}", status=500)

        billing_details = stripe_charge.billing_details
        total = round(stripe_charge.amount / 100, 2)

        user_id = intent.metadata.user_id
        if not user_id:
            return HttpResponse(
                content="User ID not found in payment intent metadata.",
                status=400
            )
        try:
            profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return HttpResponse(
                content=(
                    f"UserProfile with username {profile.username} \
                    does not exist."
                ),
                status=400
            )
        # Get the subscription for the user
        try:
            subscription = Subscription.objects.get(user=profile.user)
            donation_breakdown = subscription.sub_breakdown
        except Subscription.DoesNotExist:
            return HttpResponse(
                content=(
                    f"Subscription for user {profile.username} "
                    "does not exist."
                    ),
                status=400
            )

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
                    donation_breakdown=donation_breakdown,
                )
            except Exception as e:
                if donation:
                    donation.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | SUCCESS: '
                f'Created donation in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)
