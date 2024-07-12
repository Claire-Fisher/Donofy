from django.contrib import admin
from .models import Donation


class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'user_profile',
        'date',
        'total',
        'donation_breakdown'
    )
    search_fields = ('user', 'date')

    fieldsets = (
        (None, {
            'fields': ('user_profile', 'date', 'total', 'donation_breakdown')
        }),
    )


admin.site.register(Donation, DonationAdmin)
