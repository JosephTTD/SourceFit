from django.test import TestCase, Client
from django.urls import reverse
from Users.models import CustomUser, DietData, Activity, Goal

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.home = reverse('Users-home')
        self.display_diet = reverse('')

    def test_home_GET(self):
        response = self.client.get(self.home)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Users/index.html')

    def test_display_diet_GET(self):
        response = self.client.get(self)