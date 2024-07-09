from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from charities.models import Charity
from subscriptions.models import Subscription, Donation
from django.contrib import messages
import datetime
from django.utils import timezone
from django.http import JsonResponse


# Helper functions for commonly used function variables
def get_user_profile(user):
    return get_object_or_404(UserProfile, user=user)


def get_subscription(user):
    return Subscription.objects.get_or_create(user=user)


def get_charity_favs(user_profile):
    charity_ids = user_profile.charity_favs or []
    charity_objects = Charity.objects.filter(id__in=charity_ids)
    # Filter only the charity objects with active=True
    active_charities = charity_objects.filter(active=True)
    charity_favs = [charity.id for charity in active_charities]

    return charity_favs


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
def toggle_subscription_active(request):
    """ Toggle subscription active status """
    user = request.user
    subscription, _ = get_subscription(user)

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

        # Get today's date
        today = timezone.now().date()
        today_month = today.month
        today_year = today.year

        """ Check if a donation for that user,
            with matching month and year, already exists """
        existing_donation = Donation.objects.filter(
            user=user,
            date__month=today_month,
            date__year=today_year
        ).first()

        if existing_donation:
            # Update the donation if it exists
            existing_donation.donation_active = subscription.sub_active
            existing_donation.save()
        else:
            pass

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')


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
        subscription.date = timezone.now().date()

        subscription.save()

        # Get today's date
        today = timezone.now().date()
        today_month = today.month
        today_year = today.year

        """ Check if a donation for that user,
            with matching month and year, already exists """
        existing_donation = Donation.objects.filter(
            user=user,
            date__month=today_month,
            date__year=today_year
        ).first()

        if existing_donation:
            # Update the donation if it exists
            existing_donation.donation_active = subscription.sub_active
            existing_donation.amount = subscription.sub_total
            existing_donation.donation_breakdown = subscription.sub_breakdown
            existing_donation.save()
            existing_donation._send_donation_changed_email()
        else:
            pass

    active_tab = request.GET.get('tab', 'myDonofy')

    return redirect(f'{reverse("profiles:profile")}?tab={active_tab}')


@login_required
def delete_from_favs(request, charity_id):
    """Delete a charity from a user's charity_favs list."""
    user = request.user
    user_profile = get_user_profile(user)
    charity = get_object_or_404(Charity, pk=charity_id)
    charity_favs_ids = user_profile.charity_favs or []

    if request.method == "POST":
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


def create_donation_if_24th(request):
    """
    Create a donation obj from the user's subscription if the date is the 24th.
    """
    today = timezone.now().date()

    if today.day == 24:
        # Get all active subscriptions
        active_subscriptions = Subscription.objects.filter(sub_active=True)

        for subscription in active_subscriptions:
            user = subscription.user

            # Check if a donation already exists for today
            donation_exists = Donation.objects.filter(
                user=user, date=today).exists()

            if not donation_exists:
                # Get the current sub_breakdown and sub_total
                sub_breakdown = subscription.sub_breakdown
                sub_total = subscription.sub_total

                # Create a new Donation object
                donation = Donation.objects.create(
                    user=user,
                    amount=sub_total,
                    donation_breakdown=sub_breakdown,
                )

                donation.save()
                donation._send_donation_registered_email()

    return JsonResponse({'status': 'success'})
