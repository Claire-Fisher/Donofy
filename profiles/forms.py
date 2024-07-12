from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email Address'})


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

    def __init__(self, *args, **kwargs):
        """
        Placeholders for the form
        """
        super().__init__(*args, **kwargs)
        self.fields['phone_num'].widget.attrs.update(
            {'placeholder': 'Phone Number'})
        self.fields['street_address_1'].widget.attrs.update(
            {'placeholder': 'Street Address 1'})
        self.fields['street_address_2'].widget.attrs.update(
            {'placeholder': 'Street Address 2'})
        self.fields['town_or_city'].widget.attrs.update(
            {'placeholder': 'Town or City'})
        self.fields['county'].widget.attrs.update(
            {'placeholder': 'County'})
        self.fields['post_code_zip'].widget.attrs.update(
            {'placeholder': 'Post Code / Zip'})
        self.fields['country'].widget.attrs.update(
            {'placeholder': 'Country'})
