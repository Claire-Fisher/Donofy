from django.contrib import admin
from .models import Donation


class DonationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'donation_number', 'date', 'total')

    search_fields = ('full_name', 'donation_number', 'email')

    fieldsets = (
        (None, {
            'fields': (
                'donation_number',
                'stripe_pid',
                'user_profile',
                'full_name',
                'email',
                'phone_number',
                'country',
                'postcode',
                'town_or_city',
                'street_address1',
                'street_address2',
                'county',
                'total',
                'donation_breakdown',
                'date',
            ),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['donation_number', 'date']
        return []


admin.site.register(Donation, DonationAdmin)
