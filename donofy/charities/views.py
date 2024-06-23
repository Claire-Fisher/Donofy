from django.shortcuts import render
from .models import Charity


def all_charities(request):
    """ A view to show all charities """

    charities = Charity.objects.filter(active=True)
    inactive_charities = Charity.objects.filter(active=False)

    context = {
        'charities': charities,
        'inactive_charities': inactive_charities,
    }

    return render(request, 'charities/charities.html', context)
