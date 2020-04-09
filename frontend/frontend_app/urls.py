from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('product-details/<int:id>', views.product_details, name='productDetails'),
    path('users', views.user_profile, name='userProfile'),
    path('users/edit', views.edit_user, name='editUser'),
    path('create-listing', views.create_listing),
    path('create-manufacturer', views.create_man),
    path('create-user', views.create_user)

]
