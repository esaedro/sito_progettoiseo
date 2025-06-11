from django.urls import path
from . import views

urlpatterns = [
    path('', views.eventi_home, name='eventi'),
]
