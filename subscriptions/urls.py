from django.urls import path
from . import views


urlpatterns = [
    path('manage/', views.manage_subscription, name='manage_subscription'),
]
