from django.urls import path
from . import views


app_name = 'profiles'


urlpatterns = [
    path(
        'profile/',
        views.profile,
        name='profile'
    ),
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),
]
