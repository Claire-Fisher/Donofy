from django.urls import path
from . import views


app_name = 'subscriptions'


urlpatterns = [
    path(
        'manage/',
        views.manage_subscription,
        name='manage_subscription'
    ),
    path(
        'update_subscription/',
        views.update_subscription,
        name='update_subscription'
    ),
    path(
        'delete_from_favs/<int:charity_id>/',
        views.delete_from_favs,
        name='delete_from_favs'
    ),
]
