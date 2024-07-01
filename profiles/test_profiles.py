from django.test import TestCase
from django.urls import reverse


class TestProfilesURL(TestCase):

    def test_profile_template_used(self):
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'profiles/profile.html')
