from django.shortcuts import render
from django.contrib import messages


def index(request):
    """ A view to return the index page """
    messages.info(request, 'Yay! A message!')

    return render(request, 'home/index.html')
