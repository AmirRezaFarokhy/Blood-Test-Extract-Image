from django.urls import reverse
from Main.views import HomePage
from django.test import TestCase


class ViewsTest(TestCase):

    def test_HomePage_views(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



