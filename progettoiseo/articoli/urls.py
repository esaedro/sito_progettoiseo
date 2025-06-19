from django.urls import path, include
from articoli.views import ArticleListView, ArticleDetailView, ArticleDeleteView
from . import views

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('create/', views.create_articolo, name='article-create'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('<int:pk>/update/', views.edit_articolo, name='article-edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]
