from django.shortcuts import render
from django.contrib.auth.models import User, Group
from articoli.models import Articolo
from eventi.models import Evento
from django.utils import timezone
from datetime import datetime
import json

# Create your views here.
def home(request):
    # Recupera gli ultimi 3 articoli pubblicati
    ultimi_articoli = Articolo.objects.order_by('-data_pubblicazione')[:3]

    # Recupera i 3 eventi più imminenti (con date future e stati appropriati)
    now = timezone.now()
    prossimi_eventi = Evento.objects.filter(
        inizio_evento__gt=now,
        stato__in=['IN_ATTESA', 'AL_COMPLETO']
    ).order_by('inizio_evento')[:3]

    context = {
        'ultimi_articoli': ultimi_articoli,
        'prossimi_eventi': prossimi_eventi,
    }

    return render(request, 'home.html', context)

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
