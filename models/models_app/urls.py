from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/manufacturers/', views.get_all_manufacturers, name='get_mans'),
    path('api/v1/manufacturers/<int:id>',
         views.get_or_update_manufacturer, name='get_man'),
    path('api/v1/manufacturers/<int:id>/delete/', views.delete_manufacturer),
    path('api/v1/manufacturers/create/', views.create_manufacturer),
    path('api/v1/manufacturers/get-man-id/', views.get_man_id),

    path('api/v1/products/', views.get_all_products, name='get_prods'),
    path('api/v1/products/<int:id>', views.get_or_update_product, name='get_prod'),
    path('api/v1/products/<int:id>/delete/', views.delete_product),
    path('api/v1/products/create/', views.create_product, name='create_prod'),

    path('api/v1/users/', views.get_all_users, name='get_users'),
    path('api/v1/users/<int:id>', views.get_or_update_user, name='get_user'),
    path('api/v1/users/create/', views.create_user, name='create_user'),
    path('api/v1/users/<int:id>/delete/', views.delete_user),
    path('api/v1/users/get-user-id/', views.get_user_id),


    path('account/login', views.login),
    path('account/logout', views.logout),
    path('account/get-create-token/', views.get_or_create_token),
    path('account/change-password/', views.change_password),

    path('selenium', views.selenium),

    path('api/v1/recommendations/get-or-create/<int:id>',
         views.get_or_create_recommendation),
    path('api/v1/recommendations/update/<int:id>',
         views.update_recommendation),
    path('api/v1/recommended-products/<int:id>', views.get_recommendations)

]
