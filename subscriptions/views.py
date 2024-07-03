from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile


@login_required
def manage_subscription(request):

    active_tab = request.GET.get('tab', 'myDonofy')

    context = {
        'active_tab': active_tab
    }

    return render(request, 'profiles/profile.html', context)
