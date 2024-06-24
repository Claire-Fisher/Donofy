from django.contrib import admin
from .models import Charity, Category


class CharityAdmin(admin.ModelAdmin):
    list_display = (
        'charity_name',
        'charity_num',
        'category',
        'image_url',
        'total_received',
    )

    ordering = ('charity_name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Charity, CharityAdmin)
admin.site.register(Category, CategoryAdmin)
