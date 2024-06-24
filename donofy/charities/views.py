from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Charity


def all_charities(request):
    """ A view to show all charities, including search queries """

    charities = Charity.objects.filter(active=True)
    inactive_charities = Charity.objects.filter(active=False)
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Oops! You didn't search for anything!")
                return redirect(reverse('charities'))
            
            queries = Q(charity_name__icontains=query) | Q(description__icontains=query)
            charities = Charity.objects.filter(queries, active=True)

    context = {
        'charities': charities,
        'inactive_charities': inactive_charities,
        'search_term': query,
    }

    return render(request, 'charities/charities.html', context)
