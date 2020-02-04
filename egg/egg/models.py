from django.db import models

class User(models.Model):
    """General user of the system. aka Customer/viewers."""
    userID = models.Charfield(max_length=20)
    username = models.Charfield(max_length=50)
    password = models.Charfield(max_length=50)
    numReviews = models.intergerField()
    
    #TODO : Default CreditCard option, favorites/wishlist,

class Seller(models.Model):
    """Product sellers aka other users. Perhaps this can just be a boolean flag?"""
    sellerID = models.Charfield(max_length=20)
    name = models.Charfield(max_length=50)
    productNum = models.intergerField()


class Product(models.Model):
    """Where every product will be categorized under."""
    producID = models.CharField(max_length=50)
    productType = models.Charfield(max_length=50)
    brand = models.Charfield(max_length=20)
    name = models.Charfield()
    reviewCount = models.intergerField()
    price = models.intergerField();

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

class Purchase(models.Model):
    """Transaction between cutomer and seller"""
    transactionID = models.Charfield(max_length=20)
    productID = models.Charfield(max_length=20)
    userID = models.Charfield(max_length=20)
    
    