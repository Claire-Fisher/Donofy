import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from profiles.models import UserProfile
from subscriptions.models import Subscription, Donation


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


@login_required
def staff_action(request):
    """ A view to access the staff_actions page """
    if not request.user.is_superuser:

        messages.error(
            request,
            'You do not have permissions for that. '
            'Please log in as an authorised user.'
        )
        return redirect('home/index.html')

    return render(request, 'home/staff-action.html')


@login_required
def action_payments(request):
    """
    A view for superusers to charge all users with active subscriptions
    and active donations this month
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            'You do not have permissions for that. '
            'Please log in as an authorized user.'
        )
        return redirect('home/index.html')

    stripe.api_key = settings.STRIPE_SECRET_KEY
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    # Fetch all active subscriptions and donations for the current month
    subscriptions = Subscription.objects.filter(sub_active=True)
    donations = Donation.objects.filter(
        donation_active=True,
        date__year=current_year,
        date__month=current_month
    )

    success_count = 0
    error_count = 0

    for subscription in subscriptions:
        user = subscription.user
        user_profile = UserProfile.objects.filter(user=user).first()

        if user_profile and user_profile.stripe_customer_id:
            for donation in donations.filter(user=user):
                # Skip if the donation has already been charged
                if donation.status == 'charged':
                    continue

                try:
                    # Create a Charge for the donation amount
                    charge = stripe.Charge.create(
                        # Convert pounds to pence
                        amount=int(donation.amount * 100),
                        currency='gbp',
                        customer=user_profile.stripe_customer_id,
                        source=user_profile.stripe_payment_method_id,
                        description=f"Donation for {user.username}",
                    )

                    if charge.status == 'succeeded':
                        # Update donation record if charge was successful
                        donation.status = 'charged'
                        donation.save()
                        success_count += 1
                    else:
                        messages.error(
                            request,
                            f"Failed to process payment for "
                            f"{user.username}: {charge.failure_message}"
                        )
                        error_count += 1

                except stripe.error.StripeError as e:
                    messages.error(
                        request,
                        f"Error processing payment for "
                        f"{user.username}: {str(e)}"
                    )
                    error_count += 1

    messages.success(
        request,
        f"Payments processed. Success: {success_count}, Errors: {error_count}")

    return redirect('home/index.html')
