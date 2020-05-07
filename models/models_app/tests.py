from django.test import Client, TransactionTestCase
from django.urls import reverse
from .models import Manufacturer, Product, User
import urllib.request
import urllib.parse
import json


class ManufacturerTests(TransactionTestCase):
    client = Client()

    def setUp(self):
        Manufacturer.objects.create(
            man_name="Asus", web_url="google.com", phone_num=1234)

#     def test_get_mans(self):
#         response = self.client.get(reverse('get_mans'))
#         self.assertContains(response, 'allManufacturers')

#     def test_get_man_pass(self):
#         response = self.client.get(reverse('get_man', kwargs={'id': 1}))
#         self.assertContains(response, 'man_id')

#     def test_get_man_fail(self):
#         response = self.client.get(reverse('get_man', kwargs={'id': 2}))
#         self.assertContains(response, 'error')


class ProductTests(TransactionTestCase):
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
        Product.objects.create(
            type="Monitor",
            man_id=2,
            name="Another good Monitor",
            description="Its yet another good one",
            price=246,
            warranty="2 years"
        )
        Product.objects.create(
            type="GPU",
            man_id=3,
            name="RTX 3080",
            description="Strongest gpu not yet released",
            price=930,
            warranty="1 year"
        )

    def test_get_products(self):
        response = self.client.get(reverse('get_prods'))
        self.assertContains(response, 'allProducts')

    def test_get_product_gpu(self):
        response = self.client.get(reverse('get_prod',kwargs={'id': 3}))
        self.assertEqual(response.json()['name'], 'RTX 3080')

    def test_get_product_gpu_desc(self):

        response = self.client.get(reverse('get_prod',kwargs={'id': 3}))
        self.assertEqual(response.json()['description'], 'Strongest gpu not yet released')

    # def test_post_cpu_name(self):
    #     newprod = {
    #         'type':"CPU",
    #         'man_id':1,
    #         'img_url':'p',
    #         'name':"Intel i9 8990K",
    #         'description':"I hope this works",
    #         'price':430,
    #         'warranty':"1 year",
    #         'product_img':""
    #     }
    #     response = self.client.post(reverse('create_prod'), newprod)
    #     # print(response.json())
    #     self.assertEqual(response.json()['name'], 'Intel i9 8990K')

    

    def test_get_product_gpu(self): 
        response = self.client.get(reverse('get_prod',kwargs={'id': 1}))
        #print(response.json())
        self.assertEqual(response.json()['type'], 'Monitor')

    # def test_get_product_pass(self):
    #     response = self.client.get(reverse('get_prod', kwargs={'id': 1}))
    #     self.assertContains(response, 'product_id')

    def test_get_product_fail(self):
        response = self.client.get(reverse('get_prod', kwargs={'id': 4}))
        self.assertContains(response, 'error')


class UserTests(TransactionTestCase):
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

    def test_post_user_email_check(self):
        newuser = {
            'email':'bc',
            'username':'bc',
            'password':'bc',
            'phone_number':'bc',
            'first_name':'bc',
            'last_name':'bc',
        }
        response = self.client.post('/api/v1/users/create/', newuser)
        self.assertContains(response, 'email')
    
    def test_post_user_lname_check(self):
        newuser = {
            'email':'bc',
            'username':'bc',
            'password':'bc',
            'phone_number':'bc',
            'first_name':'bc',
            'last_name':'bc',
        }
        response = self.client.post('/api/v1/users/create/', newuser)
        self.assertContains(response, 'last_name')

    def test_post_user_pword_check(self):
        newuser = {
            'email':'bc',
            'username':'bc',
            'password':'bc',
            'phone_number':'bc',
            'first_name':'bc',
            'last_name':'bc',
        }
        response = self.client.post('/api/v1/users/create/', newuser)
        self.assertContains(response, 'password')
    
    def test_post_user_fname_check(self):
        newuser = {
            'email':'bc',
            'username':'bc',
            'password':'bc',
            'phone_number':'bc',
            'first_name':'bc',
            'last_name':'bc',
        }
        response = self.client.post('/api/v1/users/create/', newuser)
        self.assertContains(response, 'first_name')
    
    def test_post_user_pho_num_check(self):
        newuser = {
            'email':'bc',
            'username':'bc',
            'password':'bc',
            'phone_number':'bc',
            'first_name':'bc',
            'last_name':'bc',
        }
        response = self.client.post('/api/v1/users/create/', newuser)
        self.assertContains(response, 'phone_number')
    
    def test_post_user_password_check(self):
        newuser = {
            'email':'bc',
            'username':'bc',
            'password':'bc',
            'phone_number':'bc',
            'first_name':'bc',
            'last_name':'bc',
        }
        response = self.client.post('/api/v1/users/create/', newuser)
        self.assertContains(response, 'password')

    def test_post_user_username_check(self):
        newuser = {
            'email':'bc',
            'username':'bc',
            'password':'bc',
            'phone_number':'bc',
            'first_name':'bc',
            'last_name':'bc',
        }
        response = self.client.post('/api/v1/users/create/', newuser)
        self.assertContains(response, 'username')
    

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
#         self.assertEquals(new_dict['man_id'], 1)=