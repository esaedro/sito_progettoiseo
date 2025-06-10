from django.urls import path
from . import views

urlpatterns = [
    path('', views.eventi, name='eventi'),
]
