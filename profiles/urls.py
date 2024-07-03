from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path(
        'add_to_favs/<int:charity_id>/',
        views.add_to_favs,
        name='add_to_favs'
    ),
]
