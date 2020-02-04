from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    """General user of the system. aka Customer/viewers."""
    userID = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    #numReviews = models.intergerField()
    phoneNum = models.CharField(max_length=14)
    
    #TODO : Default CreditCard option, Default Shipping Address, favorites/wishlist, email-unique, First & Last name, deleted bool

#TODO : Address : addr id, user id, first and last name, addr1, addr2, post code, city, phone

class Manufacturer(models.Model):
    """Product sellers aka other users. Perhaps this can just be a boolean flag?"""
    manID = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    web_URL = models.CharField(max_length=100)
    phoneNum = models.CharField(max_length=14)
    


class Product(models.Model):
    """Where every product will be categorized under."""
    productID = models.CharField(max_length=50)
    productType = models.CharField(max_length=50)
    manID = models.CharField(max_length=20)
    name = models.CharField()
    description = models.CharField(max_length=500)
    #reviewCount = models.intergerField()
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
    
    