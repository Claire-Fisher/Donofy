from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from charities.models import Charity
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
    charity_favs_ids = user_profile.charity_favs
    # Get the full charity obj, not just IDs
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)
    subscription = Subscription.objects.get(user=user)

    if request.method == "POST":
        sub_breakdown = {}
        for charity in charity_favs:
            breakdown_value = request.POST.get(f'breakdown_{charity.id}')
            if breakdown_value:
                sub_breakdown[charity.charity_name] = int(breakdown_value)

        subscription.sub_breakdown = sub_breakdown
        subscription.save()

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')


@login_required
def delete_from_favs(request, charity_id):
    """Delete a charity from a user's charity_favs list."""
    # Get user and associated UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    # Get charity favs list
    charity = get_object_or_404(Charity, pk=charity_id)
    charity_favs_ids = user_profile.charity_favs or []

    if request.method == "POST":
        if charity.id in charity_favs_ids:
            charity_favs_ids.remove(charity.id)
            user_profile.charity_favs = charity_favs_ids
            user_profile.save()
            messages.success(
                request,
                f'{charity.charity_name}'
                f' successfully removed from your favourites.'
            )
        else:
            messages.error(
                request,
                (
                    'Oops! Something went wrong. '
                    'Please refresh the page and try again.'
                )
            )

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')
