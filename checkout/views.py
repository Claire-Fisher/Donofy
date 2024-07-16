from django.shortcuts import (
    render, redirect, reverse, get_object_or_404)
from django.contrib import messages
from django.conf import settings

from .forms import DonationForm
from .models import Donation
from profiles.models import UserProfile, Subscription
from profiles.forms import UserProfileForm

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    user = request.user
    subscription = get_object_or_404(Subscription, user=user)

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }
        donation_form = DonationForm(form_data)

        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            pid = request.POST.get('client_secret', '').split('_secret')[0]
            donation.stripe_pid = pid
            donation.total = subscription.sub_total
            donation.donation_breakdown = subscription.sub_breakdown
            donation.user_profile = user_profile

            donation.save()

            request.session['cached_donation'] = {
                'total': donation.total,
                'donation_breakdown': donation.donation_breakdown,
                'stripe_pid': donation.stripe_pid,
                'user': user.id,
            }

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'billing-success', args=[donation.donation_number]
            ))
        else:
            messages.error(
                request,
                'There was an error with your form.'
                'Please double check your information.'
            )

    total = subscription.sub_total
    if request.method == 'POST' and donation_form.is_valid():
        total = donation.total
    else:
        # Calculate the payment amount for the payment intent
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                donation_form = DonationForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_num,
                    'postcode': profile.post_code_zip,
                    'town_or_city': profile.town_or_city,
                    'street_address1': profile.street_address_1,
                    'street_address2': profile.street_address_2,
                    'county': profile.county,
                    'country': profile.country,
                })
            except UserProfile.DoesNotExist:
                donation_form = DonationForm()
        else:
            donation_form = DonationForm()

        # Create a payment intent
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        client_secret = intent.client_secret

        print(intent)

    # Handle cases where Stripe public key might be missing
    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing.'
            'Did you forget to set it in your environment?'
        )

    template = 'checkout/checkout.html'
    context = {
        'donation_form': donation_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
        'subscription': subscription,
        'subscription_breakdown': subscription.sub_breakdown,
        'total': total,
    }

    return render(request, template, context)


def billing_success(request, donation_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    donation = get_object_or_404(Donation, donation_number=donation_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the donation
        donation.user_profile = profile
        donation.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'phone_numb': donation.phone_number,
                'country': donation.country,
                'post_code_zip': donation.postcode,
                'town_or_city': donation.town_or_city,
                'street_address_1': donation.street_address1,
                'street_address_2': donation.street_address2,
                'county': donation.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Donation successfully processed! \
        Your donation number is {donation_number}. A confirmation \
        email will be sent to {donation.email}.')

    template = 'checkout/billing_success.html'
    context = {
        'donation': donation,
    }

    return render(request, template, context)
