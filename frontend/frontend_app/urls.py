from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product-details/<int:id>', views.product_details, name='productDetails'),
    path('login', views.login, name='Login'),
    path('create-user', views.create_user, name='CreateUser'),
    path('create-manufacturer', views.create_manufacturer, name='CreateManufacturer'),
]
