from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/test/', views.test),
    path('api/v1/prod_test/', views.prod_test),
]
