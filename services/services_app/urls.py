from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/type/<str:type>/', views.filterType),
    path('api/v1/test/', views.test),
    path('api/v1/newly-added/', views.newly_added),
    path('api/v1/product-details/<int:id>', views.product_details),

]
