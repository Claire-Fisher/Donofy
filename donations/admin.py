from django.contrib import admin
from .models import Donation, TargetCharity


class DonationAdmin(admin.ModelAdmin):
    readonly_fields = (
        'donation_number',
        'user_profile',
        'subscription',
        'donation_total',
        'dontation_date',
    )
    fields = (
        'donation_number',
        'user_profile',
        'subscription',
        'donation_total',
        'donation_date'
    )