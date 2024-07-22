from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Subscription
from .forms import UserForm, UserProfileForm
from checkout.models import Donation
from charities.models import Charity


def get_charity_favs(user_profile):
    charity_ids = user_profile.charity_favs or []
    charity_objects = Charity.objects.filter(id__in=charity_ids)
    # Filter only the charity objects with active=True
    active_charities = charity_objects.filter(active=True)
    charity_favs = [charity.id for charity in active_charities]

    return charity_favs


@login_required
def profile(request):
    # Get user and UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    # Check or create a subscription object
    subscription, created = Subscription.objects.get_or_create(user=user)
    # Get charity favs list
    charity_favs_ids = get_charity_favs(user_profile)
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)
    donations_history = {}
    donations_history = Donation.objects.filter(
        user_profile=user_profile).order_by('-date')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, instance=request.user.userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profiles:profile')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    active_tab = request.GET.get('tab', 'myDetails')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
        'donations_history': donations_history,
    }

    return render(request, 'profiles/profile.html', context)


# Helper functions for commonly used function variables
def get_user_profile(user):
    return get_object_or_404(UserProfile, user=user)


def get_subscription(user):
    return Subscription.objects.get_or_create(user=user)


def get_full_charity_objs(charity_favs_ids):
    return Charity.objects.filter(id__in=charity_favs_ids)


@login_required
def manage_subscription(request):
    """
    Render user's myDonofy tab to display subscription data,
    and manage their subscription settings.
    """
    # Get user, associated UserProfile + subscription
    user = request.user
    user_profile = get_user_profile(user)
    charity_favs = get_charity_favs(user_profile)
    subscription, created = get_subscription(user)

    active_tab = request.GET.get('tab', 'myDonofy')

    context = {
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def update_subscription(request):
    """
    Allow users to manage their subscription settings.
    """
    user = request.user
    user_profile = get_user_profile(user)
    charity_favs_ids = get_charity_favs(user_profile)
    charity_favs = get_full_charity_objs(charity_favs_ids)
    subscription, _ = get_subscription(user)

    if request.method == "POST":
        sub_breakdown = {}
        for charity in charity_favs:
            breakdown_value = request.POST.get(f'breakdown_{charity.id}')
            if breakdown_value:
                sub_breakdown[charity.charity_name] = int(breakdown_value)

        subscription.sub_breakdown = sub_breakdown
        # Add all the values of the sub_breakdown dict
        sub_total = sum(sub_breakdown.values())
        subscription.sub_total = sub_total

        if sub_total >= 0:
            subscription.save()
            messages.success(request, 'Save successful')
        else:
            messages.error(
                request,
                'Total value cannot be a negative number.'
                'Please check your info and try again.'
            )

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')


@login_required
def delete_from_favs(request, charity_id):
    """Delete a charity from a user's charity_favs list."""
    user = request.user
    user_profile = get_user_profile(user)
    charity = get_object_or_404(Charity, pk=charity_id)
    charity_favs_ids = user_profile.charity_favs or []

    if charity.id in charity_favs_ids:

        charity_favs_ids.remove(charity_id)
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
