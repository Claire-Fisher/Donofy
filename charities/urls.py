from django.urls import path
from . import views


urlpatterns = [
    path(
        'charities/',
        views.all_charities,
        name='charities'
    ),
    path(
        'charity_detail/<int:charity_id>/',
        views.charity_detail,
        name='charity_detail'
    ),
    path(
        'add_to_favs/<int:charity_id>/',
        views.add_to_favs,
        name='add_to_favs'
    ),
    path(
        'deactivate_charity/<int:charity_id>/',
        views.deactivate_charity,
        name='deactivate_charity'
    ),
]
