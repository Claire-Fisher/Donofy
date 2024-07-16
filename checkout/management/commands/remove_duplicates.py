from django.core.management.base import BaseCommand
from django.db.models import Count
import uuid


class Command(BaseCommand):
    help = 'Remove duplicate stripe_pid values from Donation model'

    def handle(self, *args, **kwargs):
        from checkout.models import Donation

        duplicates = Donation.objects.values(
            'stripe_pid').annotate(count=Count('id')).filter(count__gt=1)

        for duplicate in duplicates:
            stripe_pid = duplicate['stripe_pid']
            donations = Donation.objects.filter(stripe_pid=stripe_pid)

            # Delete duplicates (Keep one, delete the rest)
            # for donation in donations[1:]:
            #     donation.delete()

            # OR: Update duplicates to have unique stripe_pid
            for donation in donations[1:]:
                donation.stripe_pid = str(uuid.uuid4())
                donation.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully removed duplicates'
        ))
