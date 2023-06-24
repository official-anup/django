
from django.contrib import admin
from django.urls import path,include
# from django import app


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    
    
]
