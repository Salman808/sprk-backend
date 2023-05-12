from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Item
from .serializers import ProductSerializer


class ProductListCreateAPIViewTest(APITestCase):
    url = reverse('products_list')  # 'product-list' is the URL name for your ListCreateAPIView

    def test_list_products(self):
        # create some test data

        # Create Item Object
        item1 = Item.objects.create(code=1)

        # Create multiple products
        product1 = Product.objects.create(item=item1, amount=1)
        product2 = Product.objects.create(item=item1, amount=10)

        # make GET request to retrieve list of products
        response = self.client.get(self.url)

        # assert response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert response data
        expected_data = ProductSerializer([product1, product2], many=True).data

        self.assertEqual(response.data.get("results"), expected_data)

        # Create a new Product Object with same Item
        product3 = Product.objects.create(item=item1, amount=3)

        # Call the Product List API
        response = self.client.get(self.url)

        expected_data = ProductSerializer([product1, product2, product3], many=True).data

        # test the response object with the expected result
        self.assertEqual(response.data.get("results"), expected_data)

    def test_create_product(self):
        # create data for POST request
        data = {'item': {'code': '1'}, 'amount': 2, 'comment': 'New Product'}

        # make POST request to create new product
        response = self.create_product(data)

        # assert response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # assert new product was created
        self.assertTrue(Product.objects.filter(item__code=1).exists())

        # assert response data
        expected_data = {'id': Product.objects.get(item__code=1).id, 'comment': 'New Product', 'amount': 2,
                         'item': {'code': '1'}}
        # test the response object with the expected result
        self._check_response(response.data, expected_data)

    def test_retrieve_product(self):
        # create New Product
        code = 10121
        data = {'item': {'code': code}, 'amount': 6, 'comment': 'New ITEM Product'}

        response = self.create_product(data)

        # assert response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # assert new product was created
        self.assertFalse(Product.objects.filter(item__code=1).exists())

        # assert response data
        expected_data = {'id': Product.objects.get(item__code=code).id, 'comment': 'New ITEM Product', 'amount': 6,
                         'item': {'code': '10121'}}

        # test the response object with the expected result
        self._check_response(response.data, expected_data)

        # call the get API with the code
        response = self.client.get(f"{self.url}{code}")
        self._check_response(response.data.get("results")[0], expected_data)

    def create_product(self, data):
        # make POST request to create new product
        return self.client.post(self.url, data, format='json')

    def _check_response(self, response, expected_data):
        # assert the response data and expected data
        self.assertEqual(response.get('id'), expected_data.get('id'))
        self.assertEqual(response.get('comment'), expected_data.get('comment'))
        self.assertEqual(response.get('amount'), expected_data.get('amount'))
        self.assertEqual(response.get('item').get('code'), expected_data.get('item').get('code'))
