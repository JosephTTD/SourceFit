from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUrls(SimpleTestCase):

    def testListUrlIsResolved(self):
        url = reverse('')