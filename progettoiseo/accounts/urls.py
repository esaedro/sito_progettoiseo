from django.urls import path
from . import views

urlpatterns = [
    path('registrazione/', views.registrazione, name='registrazione'),
    path('profilo/', views.modifica_profilo, name='profilo'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('logout-success/', views.logout_success, name='logout_success'),
    path('modifica-password/', views.modifica_password, name='modifica-password')
]
