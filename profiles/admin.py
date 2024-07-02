from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserProfileAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
