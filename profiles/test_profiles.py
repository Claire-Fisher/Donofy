from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestProfilesURL(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@email.com'
        )

    def test_profile_template_used(self):
        self.client.login(
            username='testuser',
            password='testpassword123',
            email='testuser@email.com'
        )
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'profiles/profile.html')
