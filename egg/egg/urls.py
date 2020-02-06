from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from app.models import models
from app import views 
=======
from django.urls import include, path
>>>>>>> master

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
