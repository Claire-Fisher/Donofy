import stripe
from django.conf import settings
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from charities.models import Charity
from subscriptions.models import Subscription, Donation
from .forms import UserForm, UserProfileForm


def get_charity_favs(user_profile):
    charity_ids = user_profile.charity_favs or []
    charity_objects = Charity.objects.filter(id__in=charity_ids)
    # Filter only the charity objects with active=True
    active_charities = charity_objects.filter(active=True)
    charity_favs = [charity.id for charity in active_charities]

    return charity_favs


@login_required
def profile(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    # Get user and UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    user_form = UserForm(instance=user)
    user_profile_form = UserProfileForm(instance=user_profile)
    # Check or create a subscription object
    subscription, created = Subscription.objects.get_or_create(user=user)
    # Get charity favs list
    charity_favs_ids = get_charity_favs(user_profile)
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)

    active_tab = request.GET.get('tab', 'myDetails')

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
        'stripe_public_key': stripe_public_key,
        'client_secret': 'test client secret',
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def save_card(request):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_SECRET_KEY

        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)

        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(
            request.POST, instance=user_profile
        )

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
        else:
            messages.error(
                request,
                'Update failed. Please ensure the form is valid.'
            )
            return redirect('profiles:update_profile')

        # Check for payment consent
        if 'consent' not in request.POST or not request.POST.get('consent'):
            messages.error(request, 'You must consent to payment processing.')
            return redirect('profiles:update_profile')

        setup_intent_id = request.POST.get('setup_intent_id')
        if not setup_intent_id:
            messages.error(request, 'Setup Intent ID is missing.')
            return redirect('profiles:profile')

        try:
            # Retrieve the SetupIntent
            setup_intent = stripe.SetupIntent.retrieve(setup_intent_id)
            payment_method_id = setup_intent.payment_method

            # Check if the user already has a Stripe customer ID
            if user_profile.stripe_customer_id:
                # Attach the payment method to the existing customer
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=user_profile.stripe_customer_id
                )
            else:
                # Create a new customer and attach the payment method
                customer = stripe.Customer.create(
                    payment_method=payment_method_id,
                    invoice_settings={
                        'default_payment_method': payment_method_id
                    }
                )
                user_profile.stripe_customer_id = customer.id
                user_profile.save()

            # Set the payment method as the default for future invoices
            stripe.Customer.modify(
                user_profile.stripe_customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )

            messages.success(request, 'Card details saved successfully.')
            return redirect('profiles:update_profile')

        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {str(e)}")
            return redirect('profiles:update_profile')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('profiles:update_profile')

    else:
        return redirect('profiles:update_profile')
