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
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Check for payment consent
        if 'consent' not in request.POST or not request.POST.get('consent'):
            messages.error(request, 'You must consent to payment processing.')
            return redirect('profiles:update_profile')

        user_profile = UserProfile.objects.get(user=request.user)
        user_data = {
            'name': f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'address': {
                'line1': user_profile.street_address_1,
                'line2': user_profile.street_address_2,
                'city': user_profile.town_or_city,
                'state': user_profile.county,
                'postal_code': user_profile.post_code_zip,
                'country': user_profile.country.code
            },
            'phone': user_profile.phone_num,
            'metadata': {
                'consent': 'true'
            }
        }

        try:
            # Check if the user already has a Stripe customer ID
            if user_profile.stripe_customer_id:
                customer = stripe.Customer.modify(
                    user_profile.stripe_customer_id, **user_data
                )
            else:
                # Create a new customer
                customer = stripe.Customer.create(**user_data)
                user_profile.stripe_customer_id = customer['id']
                user_profile.save()

            # Create a SetupIntent for future payments
            setup_intent = stripe.SetupIntent.create(
                customer=user_profile.stripe_customer_id,
                payment_method_types=["card"]
            )

            return render(request, 'profiles/billing-success.html', {
                'client_secret': setup_intent.client_secret
            })

        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {str(e)}")
            return redirect('profiles:update_profile')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('profiles:update_profile')
    else:
        return redirect('profiles:update_profile')
