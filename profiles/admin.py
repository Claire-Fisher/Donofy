from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Subscription
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserProfileAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_active', 'sub_total')
    search_fields = ('user__username', 'user__last_name', 'user__email')
    list_filter = ('sub_active',)

    fieldsets = (
        (None, {
            'fields': ('user', 'sub_active', 'sub_total', 'sub_breakdown')
        }),
    )


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
