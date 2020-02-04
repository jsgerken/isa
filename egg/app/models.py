from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14)
    
    #TODO : Default CreditCard option, Default Shipping Address, favorites/wishlist, email-unique, First & Last name, deleted bool
    #TODO : Address : addr id, user id, first and last name, addr1, addr2, post code, city, phone

class Manufacturer(models.Model):
    man_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    web_url = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=14)

class Product(models.Model):
    product_id = models.CharField(max_length=50)
    product_type = models.CharField(max_length=50)
    man_id = models.CharField(max_length=20)
    name = models.CharField()
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    warrenty = models.IntegerField()

# class SearchFilters(models.Model):
#     """The many ways to sort through what is listed on the site to narrow down searches"""
#     COMPONENT_TYPE = [
#         ('CPU', 'CPU'),
#         ('MOBO', 'MotherBoard'),
#         ('RAM', 'Memory'),
#         ('GPU', 'Video Cards'),
#         ('PSU', 'Power Supply'),
#         ('CASE', 'Computer Case'),
#         ('FAN', 'Fans')
#         ('HDD', 'Hard Drive')
#         ('SSD', 'Solid State Drives')
#     ]
#     search_type_filter=models.CharField(
#         choice=COMPONENT_TYPE,
#     )

# class Purchase(models.Model):
#     """Transaction between cutomer and seller"""
#     transactionID = models.Charfield(max_length=20)
#     productID = models.Charfield(max_length=20)
#     userID = models.Charfield(max_length=20)
    
    