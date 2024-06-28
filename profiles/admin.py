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
        'first_name',
        'last_name',
        'phone_number',
        'street_address_1',
        'street_address_2',
        'town_or_city',
        'country',
    )

    list_display = (
        'charity_favs',
    )

    ordering = ('last_name',)


admin.site.register(UserProfile, UserProfileAdmin)
