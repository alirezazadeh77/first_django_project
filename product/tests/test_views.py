from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse as api_reverse

from product.models import Category


class TestProduct(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="test category", properties={'color': 'string'})
        self.test_client = APIClient()

    def test_api_categories(self):
        # self.assertEqual(Category.objects.count(), 1 )
        category_url = api_reverse('ca-list')
        category_r = self.test_client.get(path=category_url)
        self.assertEqual(category_r.status_code, status.HTTP_200_OK)
        self.assertContains(category_r, 'test category', status_code=status.HTTP_200_OK)
        # self.assertEqual(category_r.json().get('cont'), 1)
