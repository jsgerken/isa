
from django.contrib import admin
from django.urls import path
from app.models import models
from app import views 
from . import views 

urlpatterns = [
    path('api/v1/products', views.Products),
    #/api/v1/products/id
    #/api/v1/products/create
    #/api/v1/products/id/delete
]

urlpatterns = [
    path('api/v1/manufacturers/', views.get_all_manufacturers),
    path('api/v1/manufacturers/<int:id>', views.get_or_update_manufacturer),
    path('api/v1/manufacturers/<int:id>/delete/', views.delete_manufacturer),
    path('api/v1/manufacturers/create/', views.create_manufacturer),
]
