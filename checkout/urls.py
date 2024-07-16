from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path(
        'billing_success/<donation_number>',
        views.billing_success,
        name='billing_success'
    ),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'
    ),
    path('wh/', webhook, name='webhook'),
]
