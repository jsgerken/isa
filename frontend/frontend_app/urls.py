from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product-details/<int:id>', views.product_details, name='productDetails'),
    path('create-listing', views.create_listing),
    path('password-reset/', views.password_reset),
    path('password-reset-confirm/<uidb64>/<token>/<is_user>/',  # need to add is_user to this
         views.password_reset_confirm, name='password_reset_confirm')
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']

]
