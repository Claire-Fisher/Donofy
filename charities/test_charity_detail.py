from django.test import TestCase
from django.urls import reverse
from .models import Charity

class TestCharityDetailURL(TestCase):

    def setUp(self):
        self.charity1 = Charity.objects.create(
            id=1,
            charity_name='C Test-Charity 1',
            active=True,
            charity_num=123,
            description='Test description 1',
            total_received_monthly={},
        )

    def test_charity_detail_template_used(self):
        response = self.client.get(reverse('charity_detail', args=[self.charity1.id]))
        self.assertTemplateUsed(response, 'charities/charity_detail.html')
