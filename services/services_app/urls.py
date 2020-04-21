from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/top/', views.get_top_viewed),
    path('api/v1/newly-added/', views.newly_added),
    path('api/v1/product-details/<int:id>', views.product_details),
    path('api/v1/users/<int:id>', views.user_profile),
    path('api/v1/sort/<str:attribute>', views.sort_products),
    path('api/v1/man/<int:product_id>', views.get_man_from_product),
    path('api/v1/create-account', views.create_account),
    path('api/v1/login', views.login),
    path('api/v1/logout', views.logout),
    path('api/v1/create-new-listing', views.create_new_listing),
    # path('api/v1/send-email', views.send_email),
    path('api/v1/reset-password/', views.reset_password),
    path('api/v1/reset-password-confirm/', views.reset_password_confirm),
    path('api/v1/change-password/', views.change_password)


]
