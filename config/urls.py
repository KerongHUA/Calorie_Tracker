from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('profiles.urls')),
    path('', include('foods.urls')),
    path('', include('intake.urls')),
]