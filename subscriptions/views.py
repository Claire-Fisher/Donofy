from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from subscriptions.models import Subscription
from django.contrib import messages


@login_required
def manage_subscription(request):
    """
    Render user's myDonofy tab to display subscription data,
    and manage their subscription settings.
    """
    # Get user, associated UserProfile + subscription
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    # Get user charity_favs & subscription or creates empty ones if not found.
    charity_favs = user_profile.charity_favs or []
    subscription, created = Subscription.objects.get_or_create(user=user)

    active_tab = request.GET.get('tab', 'myDonofy')

    context = {
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def toggle_subscription_active(request):
    """ Toggle subscription active status """
    user = request.user
    subscription = Subscription.objects.get(user=user)

    if request.method == "POST":
        if subscription.sub_active:
            subscription.sub_active = False
            messages.info(
                request, 'Your donations have been paused.')
            subscription.save()
        else:
            subscription.sub_active = True
            messages.success(
                request, 'Hooray! Your donations are active! You are awesome!')
            subscription.save()

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')


@login_required
def update_subscription(request):
    """
    Allow users to manage their subscription settings.
    """
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    charity_favs = user_profile.charity_favs
    subscription = Subscription.objects.get(user=user)

    if request.method == "POST":
        sub_breakdown = {}
        for charity in charity_favs:
            breakdown_value = request.POST.get(f'breakdown_{charity.id}')
            if breakdown_value is not None:
                sub_breakdown.append[str(charity.id)] = int(breakdown_value)

        subscription.sub_breakdown = sub_breakdown
        subscription.save()

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')
