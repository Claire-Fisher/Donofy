import stripe
from django.conf import settings
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from charities.models import Charity
from subscriptions.models import Subscription
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
def update_profile(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    # Get user and associated UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    # Check or create a subscription object
    subscription, created = Subscription.objects.get_or_create(user=user)
    # Get charity favs list
    charity_favs_ids = user_profile.charity_favs or []
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(
            request.POST, instance=user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, 'Billing details updated successfully.')
            return redirect(f"{reverse('profiles:profile')}?tab=myDetails")
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        user_form = UserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user_profile)

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
    """
    A view to save or update a user's card payment details with Stripe
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        stripe_token = request.POST.get('stripeToken')

        if stripe_token:
            try:
                # Check if the user has a Stripe customer ID
                if user_profile.stripe_customer_id:
                    # Retrieve the existing customer from Stripe
                    customer = stripe.Customer.retrieve(
                        user_profile.stripe_customer_id)
                    # Update the customer with the new payment source
                    customer.source = stripe_token
                    customer.address = {
                        'line1': user_profile.street_address_1,
                        'line2': user_profile.street_address_2,
                        'city': user_profile.town_or_city,
                        'state': user_profile.county,
                        'postal_code': user_profile.post_code_zip,
                        'country': user_profile.country,
                    }
                    customer.save()
                else:
                    # Create a new customer object
                    customer = stripe.Customer.create(
                        email=user.email,
                        source=stripe_token,
                        address={
                            'line1': user_profile.street_address_1,
                            'line2': user_profile.street_address_2,
                            'city': user_profile.town_or_city,
                            'state': user_profile.county,
                            'postal_code': user_profile.post_code_zip,
                            'country': user_profile.country,
                        }
                    )
                    user_profile.stripe_customer_id = customer.id
                
                # Save the user profile with the Stripe customer ID
                user_profile.save()

                messages.success(
                    request, 'Your card details have been saved successfully.')
            except stripe.error.StripeError as e:
                messages.error(request, f"Error saving card: {str(e)}")
        else:
            messages.error(request, "Invalid payment information.")

    # Prepare context for rendering the profile page
    user_profile = get_object_or_404(UserProfile, user=user)
    user_form = UserForm(instance=user)
    user_profile_form = UserProfileForm(instance=user_profile)
    active_tab = request.GET.get('tab', 'myDetails')
    charity_favs_ids = get_charity_favs(user_profile)
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)
    subscription, created = Subscription.objects.get_or_create(user=user)

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'profiles/profile.html', context)
