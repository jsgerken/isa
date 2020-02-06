
from django.contrib import admin
from django.urls import path
from app.models import models
from app import views 

urlpatterns = [
    path('api/v1/products', views.Products),
    #/api/v1/products/id
    #/api/v1/products/create
    #/api/v1/products/id/delete
]
