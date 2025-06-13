# views.py - Versione corretta
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Articolo

class ArticleListView(ListView):
    model = Articolo
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 9  # Opzionale: per la paginazione
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data_pubblicazione')  # Cambiato da 'created_at' a 'data_pubblicazione'
        tag_filter = self.request.GET.get('tag')
        if tag_filter:
            queryset = queryset.filter(tag__icontains=tag_filter)  # Cambiato da 'tags' a 'tag'
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggiungi i tag disponibili per il filtro
        available_tags = set()
        for article in Articolo.objects.all():
            if article.tag:  # Cambiato da 'tags' a 'tag'
                tags = [tag.strip().replace('#', '') for tag in article.tag.split(',')]
                available_tags.update(tags)
        context['available_tags'] = sorted(available_tags)
        return context

# CORREZIONE: Cambiato da ListView a DetailView
class ArticleDetailView(DetailView):
    model = Articolo
    template_name = 'article_detail.html'
    context_object_name = 'article'

@method_decorator(permission_required('articoli.add_articolo'), name='dispatch')
class ArticleCreateView(CreateView):
    model = Articolo
    template_name = 'article_form.html'
    fields = '__all__'
    success_url = reverse_lazy('article-list')

@method_decorator(permission_required('articoli.change_articolo'), name='dispatch')  # Permesso più appropriato
class ArticleUpdateView(UpdateView):
    model = Articolo
    template_name = 'article_form.html'
    fields = '__all__'
    success_url = reverse_lazy('article-list')
    
    def get_success_url(self):
        # Opzionale: reindirizza al dettaglio dell'articolo dopo la modifica
        return reverse_lazy('article-detail', kwargs={'pk': self.object.pk})

@method_decorator(permission_required('articoli.delete_articolo'), name='dispatch')  # Permesso più appropriato
class ArticleDeleteView(DeleteView):
    model = Articolo
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article-list')