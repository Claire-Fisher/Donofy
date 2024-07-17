from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from profiles.models import UserProfile
from django.db.models.functions import Lower
from .models import Charity


def all_charities(request):
    """ A view to show all charities, including search queries """

    charities = Charity.objects.filter(active=True)
    inactive_charities = Charity.objects.filter(active=False)
    query = None
    categories = None
    sort = 'charity_name'
    direction = 'asc'

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "Oops! You didn't search for anything!")
                return redirect(reverse('charities'))

            queries = Q(
                charity_name__icontains=query) | Q(
                    description__icontains=query)
            charities = charities.filter(queries)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            charities = charities.filter(category__name__in=categories)

        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort == 'charity_name':
                charities = charities.annotate(
                    lower_name=Lower('charity_name'))
                sort = 'lower_name'

        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sort = f'-{sort}'

    charities = charities.order_by(sort)

    # Get user and associated UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    charity_favs_ids = user_profile.charity_favs or []
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)

    context = {
        'charities': charities,
        'inactive_charities': inactive_charities,
        'search_term': query,
        'current_categories': categories,
        'charity_favs': charity_favs,
    }

    return render(request, 'charities/charities.html', context)


def charity_detail(request, charity_id):
    """ A view to show individual charity details """

    charity = get_object_or_404(Charity, pk=charity_id)
    # Get user and associated UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    charity_favs_ids = user_profile.charity_favs or []
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)

    context = {
        'charity': charity,
        'charity_favs': charity_favs,
    }

    return render(request, 'charities/charity_detail.html', context)


@login_required
def add_to_favs(request, charity_id):
    """ Add a charity to a user's charity_favs list """
    # Get user and associated UserProfile
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    charity = get_object_or_404(Charity, pk=charity_id)
    charities = Charity.objects.filter(active=True)
    inactive_charities = Charity.objects.filter(active=False)
    query = None
    categories = None

    # Get charity favs list
    charity_favs_ids = user_profile.charity_favs or []
    charity_favs = Charity.objects.filter(id__in=charity_favs_ids)

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
                request, f'Added {charity.charity_name} to your favourites'
            )

    context = {
        'charities': charities,
        'inactive_charities': inactive_charities,
        'search_term': query,
        'current_categories': categories,
        'charity_favs': charity_favs,
    }

    return render(request, 'charities/charities.html', context)


@login_required
def deactivate_charity(request, charity_id):
    charity = get_object_or_404(Charity, pk=charity_id)
    charity.active = False
    charity.save()
    messages.success(
        request,
        f'{charity.charity_name} has been deactivated.'
        'This can be reactivated in the site admin'
        )

    return redirect('charities')
