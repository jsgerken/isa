from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_deleted = models.BooleanField(blank=True)

# class Address(models.Model):
#    addr id, user id, first and last name, addr1, addr2, post code, city, phone


class Manufacturer(models.Model):
    man_id = models.AutoField(primary_key=True)
    man_name = models.CharField(max_length=50)
    web_url = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=14)


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_type = models.CharField(max_length=15)
    man_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
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
