from django.contrib import admin
from .models import Subscription, Donation


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_active', 'sub_total')
    search_fields = ('user__username', 'user__last_name', 'user__email')
    list_filter = ('sub_active',)

    fieldsets = (
        (None, {
            'fields': ('user', 'sub_active', 'sub_total', 'sub_breakdown')
        }),
    )


class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'donation_active',
        'date',
        'amount',
        'status',
        'donation_breakdown'
    )
    search_fields = ('user', 'date')

    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'amount', 'donation_breakdown')
        }),
    )


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Donation, DonationAdmin)
