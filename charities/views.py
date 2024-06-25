from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Charity, Category

def all_charities(request):
    """ A view to show all charities, including search queries """

    charities = Charity.objects.filter(active=True)
    inactive_charities = Charity.objects.filter(active=False)
    query = None
    categories = None
    sort = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            charities = charities.filter(category__id__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Oops! You didn't search for anything!")
                return redirect(reverse('charities'))

            queries = Q(charity_name__icontains=query) | Q(description__icontains=query)
            charities = charities.filter(queries)

    context = {
        'charities': charities,
        'inactive_charities': inactive_charities,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'charities/charities.html', context)
