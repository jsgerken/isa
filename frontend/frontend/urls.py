from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('frontend_app.urls')),
    path('', RedirectView.as_view(url='/home/')),
]
