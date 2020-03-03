from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/manufacturers/', views.get_all_manufacturers, name='get_mans'),
    path('api/v1/manufacturers/<int:id>',
         views.get_or_update_manufacturer, name='get_man'),
    path('api/v1/manufacturers/<int:id>/delete/', views.delete_manufacturer),
    path('api/v1/manufacturers/create/', views.create_manufacturer),

    path('api/v1/products/', views.get_all_products, name='get_prods'),
    path('api/v1/products/<int:id>', views.get_or_update_product, name='get_prod'),
    path('api/v1/products/<int:id>/delete/', views.delete_product),
    path('api/v1/products/create/', views.create_product),

    path('api/v1/users/', views.get_all_users, name='get_users'),
    path('api/v1/users/<int:id>', views.get_or_update_user, name='get_user'),
    path('api/v1/users/create/', views.create_user),
    path('api/v1/users/<int:id>/delete/', views.delete_user),
]
