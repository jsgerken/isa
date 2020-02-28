from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/manufacturers/', views.get_all_manufacturers),
    path('api/v1/manufacturers/<int:id>', views.get_or_update_manufacturer),
    path('api/v1/manufacturers/<int:id>/delete/', views.delete_manufacturer),
    path('api/v1/manufacturers/create/', views.create_manufacturer),
    path('api/v1/products/', views.get_all_products),
    path('api/v1/products/<int:id>', views.get_or_update_product),
    path('api/v1/products/<int:id>/delete/', views.delete_product),
    path('api/v1/products/create/', views.create_product),
]
