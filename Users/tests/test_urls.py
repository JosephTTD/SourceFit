from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Users.views import home_view, login_view, register_view, dashboard_view, display_diet_view, display_exercise_view, \
    display_goal_view, profile, settings


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('Users-home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home_view)

    def test_login_url_is_resolved(self):
        url = reverse('Users-login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, login_view)

    def test_register_url_is_resolved(self):
        url = reverse('Users-register')
        print(resolve(url))
        self.assertEquals(resolve(url).func, register_view)

    def test_dashboard_url_is_resolved(self):
        url = reverse('Users-dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, dashboard_view)

    def test_diet_url_is_resolved(self):
        url = reverse('Users-diet')
        print(resolve(url))
        self.assertEquals(resolve(url).func, display_diet_view)

    def test_exercise_url_is_resolved(self):
        url = reverse('Users-exercise')
        print(resolve(url))
        self.assertEquals(resolve(url).func, display_exercise_view)

    def test_goals_url_is_resolved(self):
        url = reverse('Users-goals')
        print(resolve(url))
        self.assertEquals(resolve(url).func, display_goal_view)

    def test_profile_url_is_resolved(self):
        url = reverse('Users-profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, profile)

    def test_settings_url_is_resolved(self):
        url = reverse('Users-settings')
        print(resolve(url))
        self.assertEquals(resolve(url).func, settings)

