from django.test import TestCase
from django.urls import reverse
from .models import Charity


class TestCharitiesURL(TestCase):

    def test_charities_template_used(self):
        response = self.client.get(reverse('charities'))
        self.assertTemplateUsed(response, 'charities/charities.html')


class TestCharitiesView(TestCase):

    def setUp(self):
        self.charity1 = Charity.objects.create(charity_name='Test-Charity 1', active=True, charity_num=123, description='Test description', total_received_monthly={})
        self.charity2 = Charity.objects.create(charity_name='Test-Charity 2', active=True, charity_num=123, description='Test description', total_received_monthly={})
        self.charity3 = Charity.objects.create(charity_name='Test-Charity 3', active=False, charity_num=123, description='Test description', total_received_monthly={})

    def test_view_gets_all_charities(self):
        response = self.client.get(reverse('charities'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.charity1.charity_name)
        self.assertContains(response, self.charity2.charity_name)
        self.assertEqual(len(response.context['charities']), 2)
