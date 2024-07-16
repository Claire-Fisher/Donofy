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
    path('wh/', webhook, name='webhook'),
]
