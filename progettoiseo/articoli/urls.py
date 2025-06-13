from django.urls import path, include
from articoli.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('add/', ArticleCreateView.as_view(), name='article-add'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article-edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]
