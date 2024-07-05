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
        'toggle_subscription/',
        views.toggle_subscription_active,
        name='toggle_subscription_active'
    ),
    path(
        'update_subscription/',
        views.update_subscription,
        name='update_subscription'
    ),
]
