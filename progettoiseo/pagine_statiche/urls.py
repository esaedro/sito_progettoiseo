from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('storia/', views.storia, name='storia'),
    path('contatti/', views.contatti, name='contatti'),
    path('direttivo/', views.direttivo, name='direttivo')
]
