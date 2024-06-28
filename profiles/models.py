from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    User profile model for storing user personal data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=25, blank=False, unique=True, default='default_user')
    active_user = models.BooleanField(default=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    phone_num = models.CharField(max_length=20, blank=True)
    street_address_1 = models.CharField(max_length=80, blank=True)
    street_address_2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    county = models.CharField(max_length=80, blank=True)
    post_code_zip = models.CharField(max_length=20, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=True)
    charity_favs = models.JSONField(default=list, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
