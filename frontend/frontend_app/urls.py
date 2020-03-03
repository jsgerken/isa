from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product-details/<int:id>', views.product_details, name='productDetails')

]
