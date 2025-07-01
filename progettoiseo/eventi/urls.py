from django.urls import path
from . import views


urlpatterns = [
    path('', views.event_list, name='lista_eventi'),
    path('lista/', views.event_list, name='lista_eventi'),
    path('crea/', views.event_create, name='evento-create'),
    path('<int:pk>/', views.event_detail, name='evento-detail'),
    
    path('modifica/<int:pk>/', views.event_update, name='evento-edit'),
    path('elimina/<int:pk>/', views.event_delete, name='evento-delete'),
    path('iscriviti/<int:pk>/', views.event_register, name='evento-register'),
    path('disiscriviti/<int:pk>/', views.event_unregister, name='evento-unregister'),
    #path('partecipanti/<int:event_id>/', views.event_participants, name='event_participants'),
    #path('organizzatore/<int:event_id>/', views.event_organizer, name='event_organizer'),

]
