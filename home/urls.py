from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('staff_action/', views.staff_action, name='staff_action'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
