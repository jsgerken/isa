from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # changed this field to auto
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=14)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)


class Manufacturer(models.Model):
    man_id = models.AutoField(primary_key=True)
    man_name = models.CharField(max_length=50, unique=True)
    web_url = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    password = models.CharField(max_length=1000)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    man_id = models.IntegerField()
    views = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    price = models.IntegerField()
    warranty = models.CharField(max_length=50)
    img_url = models.CharField(max_length=500)
    datetime_modified = models.DateTimeField(auto_now=True)
    datetime_created = models.DateTimeField(auto_now_add=True)


class Authenticator(models.Model):
    authenticator = models.CharField(max_length=1000)
    auth_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
