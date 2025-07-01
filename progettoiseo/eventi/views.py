from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required       
from django.urls import path
from . import views
from django.db.models.signals import post_save, m2m_changed, pre_delete, pre_save
from django.dispatch import receiver        
from .models import Evento
from django.contrib import messages
from django.urls import reverse
from django import forms
from django.shortcuts import get_object_or_404
from .forms import EventoForm
from django.http import JsonResponse

def event_list(request):
    events = Evento.objects.order_by('-inizio_evento')
    user = request.user
    is_direttivo = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Direttivo").exists())
    return render(request, 'lista_eventi.html', {'events': events, 'is_direttivo': is_direttivo})

@login_required
def event_create(request):
    user = request.user
    is_direttivo = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Direttivo").exists())
    if not is_direttivo:
        return redirect('lista_eventi')
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save()
            messages.success(request, 'Evento creato con successo!')
            return redirect(reverse('lista_eventi'))
    else:
        form = EventoForm()
    return render(request, 'form_eventi.html', {'form': form, 'is_direttivo': is_direttivo})

def event_detail(request, pk):
    event = get_object_or_404(Evento, pk=pk)
    user = request.user
    is_direttivo = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Direttivo").exists())
    return render(request, 'dettaglio_evento.html', {'event': event, 'is_direttivo': is_direttivo})

@login_required
def event_delete(request, pk):
    user = request.user
    is_direttivo = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Direttivo").exists())
    event = get_object_or_404(Evento, pk=pk)
    if not is_direttivo:
        return redirect('lista_eventi')
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Evento eliminato con successo!')
        return redirect('lista_eventi')
    return render(request, 'evento_conferma_eliminazione.html', {'object': event, 'is_direttivo': is_direttivo})

@login_required
def event_update(request, pk):
    user = request.user
    is_direttivo = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Direttivo").exists())
    event = get_object_or_404(Evento, pk=pk)
    if not is_direttivo:
        return redirect('lista_eventi')
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento aggiornato con successo!')
            return redirect('evento-detail', pk=event.pk)
    else:
        form = EventoForm(instance=event)
    return render(request, 'form_eventi.html', {'form': form, 'is_direttivo': is_direttivo, 'event': event})

@login_required
def event_register(request, pk):
    event = get_object_or_404(Evento, pk=pk)
    user = request.user
    profilo = getattr(user, 'profile', None)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if not profilo:
        msg = 'Profilo utente non trovato.'
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg})
        messages.error(request, msg)
        return redirect('evento-detail', pk=pk)
    if not event.is_iscrivibile():
        msg = 'Non ci sono posti disponibili per questo evento.'
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg})
        messages.error(request, msg)
        return redirect('evento-detail', pk=pk)
    if profilo in event.iscritti.all():
        msg = 'Sei già iscritto a questo evento.'
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg})
        messages.info(request, msg)
    else:
        event.iscritti.add(profilo)
        msg = 'Iscrizione avvenuta con successo!'
        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': msg,
                'url_unregister': reverse('evento-unregister', args=[pk]),
                'url_register': reverse('evento-register', args=[pk]),
            })
        messages.success(request, msg)
    return redirect('evento-detail', pk=pk)

@login_required
def event_unregister(request, pk):
    event = get_object_or_404(Evento, pk=pk)
    user = request.user
    profilo = getattr(user, 'profile', None)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if not profilo:
        msg = 'Profilo utente non trovato.'
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg})
        messages.error(request, msg)
        return redirect('evento-detail', pk=pk)
    if profilo in event.iscritti.all():
        event.iscritti.remove(profilo)
        msg = 'Disiscrizione avvenuta con successo!'
        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': msg,
                'url_unregister': reverse('evento-unregister', args=[pk]),
                'url_register': reverse('evento-register', args=[pk]),
            })
        messages.success(request, msg)
    else:
        msg = 'Non risulti iscritto a questo evento.'
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg})
        messages.info(request, msg)
    return redirect('evento-detail', pk=pk)
