from django.test import Client, TestCase
from django.urls import reverse
from .models import Manufacturer, Product, User
import urllib.request
import urllib.parse
import json


# class ManufacturerTests(TestCase):
#     client = Client()

#     def setUp(self):
#         Manufacturer.objects.create(
#             man_name="Asus", web_url="google.com", phone_num=1234)

#     def test_get_mans(self):
#         response = self.client.get(reverse('get_mans'))
#         self.assertContains(response, 'allManufacturers')

#     def test_get_man_pass(self):
#         response = self.client.get(reverse('get_man', kwargs={'id': 1}))
#         self.assertContains(response, 'man_id')

#     def test_get_man_fail(self):
#         response = self.client.get(reverse('get_man', kwargs={'id': 2}))
#         self.assertContains(response, 'error')


class ProductTests(TestCase):
    client = Client()

    def setUp(self):
        Product.objects.create(
            type="Monitor",
            man_id=1,
            name="Good Monitor",
            description="Hello",
            price=123,
            warranty="1 week"
        )

    def test_get_products(self):
        response = self.client.get(reverse('get_prods'))
        self.assertContains(response, 'allProducts')

    # def test_get_product_pass(self):
    #     response = self.client.get(reverse('get_prod', kwargs={'id': 1}))
    #     self.assertContains(response, 'product_id')

    def test_get_product_fail(self):
        response = self.client.get(reverse('get_prod', kwargs={'id': 2}))
        self.assertContains(response, 'error')


class UserTests(TestCase):
    client = Client()

    def setUp(self):
        User.objects.create(
            email='abc',
            username='abc',
            password='abc',
            phone_number='abc',
            first_name='abc',
            last_name='abc',
        )

    def test_get_users(self):
        response = self.client.get(reverse('get_users'))
        self.assertContains(response, 'allUsers')

    def test_get_user_pass(self):
        response = self.client.get(reverse('get_user', kwargs={'id': 1}))
        self.assertContains(response, 'user_id')

    def test_get_user_fail(self):
        response = self.client.get(reverse('get_user', kwargs={'id': 2}))
        self.assertContains(response, 'error')


# class ExperienceTests(TestCase):
#     client = Client()
#     # tests user story 2

#     def test_get_top_viewed(self):
#         req = urllib.request.Request(
#             'http://services:8000/api/v1/top/')
#         top_json = urllib.request.urlopen(req).read().decode('utf-8')
#         top_dict = json.loads(top_json)
#         products = top_dict['products']
#         self.assertTrue(products[0]['views'] > products[1]['views'])

#     # tests user story 1
#     def test_get_newest_grouping(self):
#         req = urllib.request.Request(
#             'http://services:8000/api/v1/newly-added/')
#         new_json = urllib.request.urlopen(req).read().decode('utf-8')
#         new_dict = json.loads(new_json)
#         self.assertTrue('newlyAddedSorted' in new_dict)

#     # tests user story 4
#     def test_sort_price(self):
#         req = urllib.request.Request(
#             'http://services:8000/api/v1/sort/price')
#         new_json = urllib.request.urlopen(req).read().decode('utf-8')
#         new_dict = json.loads(new_json)
#         products = new_dict['sorted']
#         self.assertTrue(products[0]['price'] > products[1]['price'])

#     #  tests user story 5
#     def test_get_man_from_product(self):
#         req = urllib.request.Request(
#             'http://services:8000/api/v1/man/1')
#         new_json = urllib.request.urlopen(req).read().decode('utf-8')
#         new_dict = json.loads(new_json)
#         self.assertEquals(new_dict['man_id'], 1)
