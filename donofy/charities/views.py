from django.shortcuts import render
from .models import Charity


def all_charities(request):
    """ A view to show all charities """

    charities = Charity.objects.all()

    context = {
        'charities': charities,
    }

    return render(request, 'charities/charities.html', context)
