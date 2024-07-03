import uuid
from django.db import models
from django.db.models import Sum
from profiles.models import UserProfile
from charities.models import Charity
from subscriptions.models import subscription


class Donation(models.Model):
    donation_number = models.CharField(
        max_length=32,
        null=False,
        editable=False,
        unique=True
    )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='donations'
    )
    selected_charities = models.JSONField(default=list, blank=False)
    donation_total = models.PositiveIntegerField(default=0, null=False)
    donation_date = models.DateField(auto_now_add=True)

    def _generate_donation_number(self):
        """
        Generate a random, unique donation number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_donation_charities_list(self):
        """
        Create a list of the target charities and save it to the donation model
        """
        self.selected_charities = []
        for target_charity in self.target_charities.all():
            charity_name = target_charity.charity.charity_name
            charity_total = target_charity.charity_total
            self.selected_charities.append(
                {charity_name: charity_total})
        self.save()

    def update_donation_total(self):
        """
        Update the donation total each time a target charity
        is added to the donation event.
        """
        self.donation_total = self.target_charities.aggregate(
            total=Sum('charity_total')
        )['total'] or 0
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the donation number
        if it doesn't already exist.
        """
        if not self.donation_number:
            self.donation_number = self._generate_donation_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.donation_number


class TargetCharity(models.Model):
    donation = models.ForeignKey(
        Donation,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='target_charities'
    )
    charity = models.ForeignKey(
        Charity,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='target_charities'
    )
    charity_total = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False
    )

    def save(self, *args, **kwargs):
        """
        Update the save method, set the charity total,
        and update the donation total.
        """
        super().save(*args, **kwargs)
        self.donation.update_donation_total()

    def __str__(self):
        return (
            f'{self.charity.charity_name}({self.charity.charity_num}), '
            f'receives=£{self.charity_total}, '
            f'on donation({self.donation.donation_number}).'
        )
