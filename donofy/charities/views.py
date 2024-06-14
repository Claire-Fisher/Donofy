from django.shortcuts import render


def charities(request):
    """ A view to return the charities page """

    return render(request, 'charities/charities.html')
