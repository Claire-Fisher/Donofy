from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path(
        'billing-success/<donation_number>',
        views.billing_success,
        name='billing_success'
    ),
]
