from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import DonationForm
from .models import Donation
from profiles.models import UserProfile, Subscription
import stripe
import json
from django.db import IntegrityError


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        donation_data = request.session.get('donation', {})
        stripe.PaymentIntent.modify(pid, metadata={
            'donation': json.dumps(donation_data),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    subscription = get_object_or_404(Subscription, user=user)

    donation_form = DonationForm()
    client_secret = ''

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
            donation.total = subscription.sub_total
            donation.donation_breakdown = subscription.sub_breakdown
            donation.user_profile = user_profile
            donation.stripe_pid = request.POST.get('stripe_pid')

            try:
                donation.save()
                request.session['save_info'] = 'save-info' in request.POST
                return redirect(
                    reverse('billing_success', args=[donation.donation_number])
                )
            except IntegrityError:
                messages.error(
                    request,
                    'A donation with this Stripe ID already exists.'
                    'Please try again.'
                )
                return redirect(reverse('checkout'))

        else:
            messages.error(
                request,
                'There was an error with your form.'
                'Please double check your information.'
            )

    if request.user.is_authenticated:
        donation_form = DonationForm(initial={
            'full_name': user_profile.user.get_full_name(),
            'email': user_profile.user.email,
            'phone_number': user_profile.phone_num,
            'postcode': user_profile.post_code_zip,
            'town_or_city': user_profile.town_or_city,
            'street_address1': user_profile.street_address_1,
            'street_address2': user_profile.street_address_2,
            'county': user_profile.county,
            'country': user_profile.country,
        })

    stripe_total = round(subscription.sub_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    client_secret = intent.client_secret

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
        'total': subscription.sub_total,
    }

    return render(request, template, context)


def billing_success(request, donation_number):
    """
    Handle successful donations
    """
    donation = get_object_or_404(Donation, donation_number=donation_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    messages.success(
        request,
        f'Donation successfully processed!'
        f'Your donation number is {donation_number}.'
        f'A confirmation email will be sent to {donation.email}.'
    )

    if 'save_info' in request.session:
        del request.session['save_info']

    template = 'checkout/billing_success.html'
    context = {
        'donation': donation,
        'profile': profile,
    }

    return render(request, template, context)
