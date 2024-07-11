import stripe
import json
from django.conf import settings
from django.shortcuts import (
    render, reverse, get_object_or_404, redirect, HttpResponse)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'subscription': json.dumps(request.session.get('subscription', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    user_form = UserForm(request.POST, instance=user)
    user_profile_form = UserProfileForm(
        request.POST, instance=user_profile
    )
    subscription = get_object_or_404(Subscription, user=user)
    if not subscription:
        messages.error(
            request,
            'You have no options set for your doantion')
        return redirect(f'{reverse("profiles:profile")}?tab=myDonofy')

    user_form - UserForm()
    user_profile_form = UserProfileForm()
    template = 'profiles:profile/billing-success.html'

    return render(request, template)
