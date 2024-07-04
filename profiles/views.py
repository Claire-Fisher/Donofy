from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from charities.models import Charity
from subscriptions.models import Subscription
from .forms import UserForm, UserProfileForm


@login_required
def profile(request):
    # Get user and associated UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    user_form = UserForm(request.POST, instance=user)
    user_profile_form = UserProfileForm(
            request.POST, instance=user_profile)
    # Check or create a subscription object
    subscription, created = Subscription.objects.get_or_create(user=user)
    # Get charity favs list
    charity_favs_ids = user_profile.charity_favs or []
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)

    active_tab = request.GET.get('tab', 'myDetails')

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def update_profile(request):
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
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        user_form = UserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user_profile)

    active_tab = request.GET.get('tab', 'myDonofy')

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
    }

    return redirect('profiles:profile', context)
