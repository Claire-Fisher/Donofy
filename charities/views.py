from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Charity, Category

def all_charities(request):
    """ A view to show all charities, including search queries """

    charities = Charity.objects.filter(active=True)
    inactive_charities = Charity.objects.filter(active=False)
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            charities = charities.filter(category__name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Oops! You didn't search for anything!")
                return redirect(reverse('charities'))

            queries = Q(charity_name__icontains=query) | Q(description__icontains=query)
            charities = charities.filter(queries)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'charity_name':
                sortkey = 'lower_name'
                charities = charities.annotate(lower_name=Lower('charity_name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            charities = charities.order_by(sortkey)

    current_sorting = f'{sort}_{direction}' if sort and direction else None

    context = {
        'charities': charities,
        'inactive_charities': inactive_charities,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'charities/charities.html', context)
