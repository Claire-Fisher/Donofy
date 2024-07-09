from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


@login_required
def staff_action(request):
    """ A view to access the staff_actions page """
    if not request.user.is_superuser:

        messages.error(
            request,
            'You do not have permissions for that. '
            'Please log in as an authorised user.'
        )
        return redirect('home/index.html')

    return render(request, 'home/staff-action.html')
