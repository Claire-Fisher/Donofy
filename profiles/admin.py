from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):

    readonly_fields = (
        'date_joined',
    )

    fields = (
        'user',
        'active_user',
        'is_authenticated',
        'first_name',
        'last_name',
        'phone_num',
        'street_address_1',
        'street_address_2',
        'town_or_city',
        'country',
        'charity_favs'
    )

    list_display = (
        'user',
        'last_name',
        'first_name',
        'active_user',
        'is_authenticated'
    )

    ordering = ('last_name',)


admin.site.register(UserProfile, UserProfileAdmin)
