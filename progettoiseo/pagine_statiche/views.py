from django.shortcuts import render
from django.contrib.auth.models import User, Group

# Create your views here.
def home(request):
    return render(request, 'home.html')

def storia(request):
    return render(request, 'storia.html')

def contatti(request):
    return render(request, 'contatti.html')

def direttivo(request):
    # Recupera tutti gli utenti che fanno parte del gruppo 'Direttivo' ordinati per ID
    try:
        gruppo_direttivo = Group.objects.get(name='Direttivo')
        membri_direttivo = User.objects.filter(groups=gruppo_direttivo).select_related('profile').order_by('id')
    except Group.DoesNotExist:
        membri_direttivo = []

    context = {
        'membri_direttivo': membri_direttivo
    }
    return render(request, 'direttivo.html', context)
