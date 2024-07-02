from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = (
            'phone_num',
            'street_address_1',
            'street_address_2',
            'town_or_city',
            'county',
            'post_code_zip',
            'country',
            )
