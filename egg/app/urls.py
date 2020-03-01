from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/manufacturers/', views.get_all_manufacturers),
    path('api/v1/manufacturers/<int:id>', views.get_or_update_manufacturer),
    path('api/v1/manufacturers/<int:id>/delete/', views.delete_manufacturer),
    path('api/v1/manufacturers/create/', views.create_manufacturer),
    # Endpoints for Users below
    path('api/v1/users/', views.get_all_users),
    path('api/v1/users/<int:id>', views.get_or_update_user),
    path('api/v1/users/create/', views.create_user),
    path('api/v1/users/<int:id>/delete/', views.delete_user),

]
