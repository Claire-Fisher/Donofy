from django.contrib import admin
from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_active', 'sub_total')
    search_fields = ('user__username', 'user__last_name', 'user__email')
    list_filter = ('sub_active',)
    readonly_fields = ('user', 'sub_total', 'sub_breakdown')

    fieldsets = (
        (None, {
            'fields': ('user', 'sub_active', 'sub_total', 'sub_breakdown')
        }),
    )


admin.site.register(Subscription, SubscriptionAdmin)
