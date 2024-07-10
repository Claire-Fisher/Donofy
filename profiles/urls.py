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
        'update_profile/',
        views.update_profile,
        name='update_profile'
    ),
    path(
        'save-card/',
        views.save_card,
        name='save_card'
    ),
]
