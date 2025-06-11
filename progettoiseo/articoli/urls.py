from django.urls import path, include
from articoli.views import ArticleListView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('articoli/', ArticleListView.as_view(), name='article-list'),
    path('articoli/add/', ArticleCreateView.as_view(), name='article-add'),
    path('articoli/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-edit'),
    path('articoli/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]
