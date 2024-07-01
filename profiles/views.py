from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """ Display the user's profile """

    return render(request, 'profiles/profile.html')
