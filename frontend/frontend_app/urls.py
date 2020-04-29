from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('product-details/<int:id>', views.product_details, name='productDetails'),
    path('users', views.user_profile, name='userProfile'),
    path('users/edit', views.edit_user, name='editUser'),
    path('create-listing', views.create_listing, name='createListing'),
    path('create-manufacturer', views.create_man),
    path('create-user', views.create_user),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('logout', views.logout),
    path('password-reset-confirm/<uidb64>/<token>/<is_man>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('search', views.search)
]
