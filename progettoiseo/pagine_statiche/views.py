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

    # Recupera i 3 eventi più imminenti (solo quelli in attesa e con date future)
    eventi = Evento.objects.all()

    # Filtra gli eventi con date future e ordina per la prima data disponibile
    eventi_futuri = []
    now = timezone.now()

    for evento in eventi:
        if evento.date_evento:  # Verifica che ci siano date
            # Converti le date da stringa a datetime per il confronto
            date_future = []
            for data_str in evento.date_evento:
                try:
                    # Assumendo formato ISO (YYYY-MM-DD) o datetime
                    if 'T' in data_str:
                        data_obj = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
                    else:
                        data_obj = datetime.strptime(data_str, '%Y-%m-%d')

                    # Rendi timezone-aware se necessario
                    if timezone.is_naive(data_obj):
                        data_obj = timezone.make_aware(data_obj)

                    if data_obj > now:
                        date_future.append(data_obj)
                except (ValueError, TypeError):
                    continue

            if date_future:
                # Aggiungi l'evento con la prima data futura per l'ordinamento
                eventi_futuri.append((evento, min(date_future)))

    # Ordina per la prima data futura e prendi i primi 3
    eventi_futuri.sort(key=lambda x: x[1])
    prossimi_eventi = [evento[0] for evento in eventi_futuri[:3]]

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
