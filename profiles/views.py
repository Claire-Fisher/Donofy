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
    # Check or create a subscription object
    subscription, created = Subscription.objects.get_or_create(user=user)

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

    # Get charity favs list
    charity_favs_ids = user_profile.charity_favs or []
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)

    active_tab = request.GET.get('tab', 'myDonofy')

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'active_tab': active_tab,
        'charity_favs': charity_favs,
        'subscription': subscription,
    }
    print("Charity Fav IDs:", charity_favs_ids)
    print("Charity Favs Count:", charity_favs.count())

    return render(request, 'profiles/profile.html', context)


@login_required
def add_to_favs(request, charity_id):
    """ Add a charity to a user's charity_favs list """
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    charity = get_object_or_404(Charity, pk=charity_id)
    redirect_url = request.POST.get('redirect_url', 'profile')

    if request.method == "POST":
        charity_favs = user_profile.charity_favs or []

        if charity.id in charity_favs:
            messages.info(
                request, 'You already have that charity in your favourites')
        else:
            charity_favs.append(charity.id)
            user_profile.charity_favs = charity_favs
            user_profile.save()
            messages.success(
                request, f"Added {charity.charity_name} to your favourites"
            )

    return redirect(redirect_url)
