from django.conf import settings
from django.shortcuts import render


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def custom_404(request, exception=None):
    """
    Render custom 404 error template
    """
    return render(request, '404.html', status=404)
