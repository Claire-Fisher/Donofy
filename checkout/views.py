import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import Subscription
from .forms import DonationForm


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    user = request.user
    subscription = get_object_or_404(Subscription, user=user)
    donation_breakdown = subscription.sub_breakdown

    if request.method == 'POST':
        if subscription.sub_total == 0:
            messages.error(
                request,
                'You have no options set for your donation'
            )
            return redirect(f'{reverse("profiles:profile")}?tab=myDonofy')

        form_data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'postcode': request.POST.get('postcode'),
            'town_or_city': request.POST.get('town_or_city'),
            'street_address1': request.POST.get('street_address1'),
            'street_address2': request.POST.get('street_address2'),
            'county': request.POST.get('county'),
            'country': request.POST.get('country'),
        }
        donation_form = DonationForm(form_data)

        if donation_form.is_valid():
            # Proceed with the payment intent creation and other logic
            total = subscription.sub_total
            stripe_total = round(total * 100)
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
            print(intent)

            if not stripe_public_key:
                messages.warning(
                    request, 
                    'Stripe public key is missing.'
                    'Did you forget to set it in your environment?'
                )
            
            context = {
                'donation_form': donation_form,
                'subscription': subscription,
                'donation_breakdown': donation_breakdown,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
            }
            return render(request, 'checkout/checkout.html', context)

    else:
        donation_form = DonationForm()

    template = 'checkout/checkout.html'
    context = {
        'donation_form': donation_form,
        'subscription': subscription,
        'donation_breakdown': donation_breakdown,
        'stripe_public_key': stripe_public_key,
    }

    return render(request, template, context)
