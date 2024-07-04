from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from subscriptions.models import Subscription
from django.contrib import messages


@login_required
def manage_subscription(request):
    # Get user and associated UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    charity_favs = user_profile.charity_favs or []

    if request.method == "POST":
        # Check for an existing user subscription
        subscription, created = Subscription.objects.get_or_create(user=user)

        subscription.sub_active = request.POST.get(
            'sub_active', subscription.sub_active) == 'on'

        subscription.sub_total = request.POST.get(
            'sub_total', subscription.sub_total)

        subscription.sub_breakdown = request.POST.get(
            'sub_breakdown', subscription.sub_breakdown)

        subscription.save()

    active_tab = request.GET.get('tab', 'myDonofy')

    context = {
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def toggle_subscription_active(request):
    user = request.user
    subscription = Subscription.objects.get(user=user)

    if request.method == "POST":
        if subscription.sub_active:
            subscription.sub_active = False
            messages.info(
                request, 'Your subscription has been paused.')
            subscription.save()
        else:
            subscription.sub_active = True
            messages.success(
                request, 'Hooray! Your donations are active! You are awesome!')
            subscription.save()

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')
