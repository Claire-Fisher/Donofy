from django.test import TestCase
from django.urls import reverse


class TestHomeURL(TestCase):

    def test_index_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/index.html')
