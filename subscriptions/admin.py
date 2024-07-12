from django.contrib import admin


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_active', 'sub_total')
    search_fields = ('user__username', 'user__last_name', 'user__email')
    list_filter = ('sub_active',)

    fieldsets = (
        (None, {
            'fields': ('user', 'sub_active', 'sub_total', 'sub_breakdown')
        }),
    )
