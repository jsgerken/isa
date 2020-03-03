from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/top/', views.get_top_viewed),
    path('api/v1/test/', views.test),
    path('api/v1/newly-added/', views.newly_added),
]
