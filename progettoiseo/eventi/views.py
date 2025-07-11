from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save, m2m_changed, pre_delete, pre_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django.utils import timezone

from . import views
from .forms import EventoForm
from .models import Evento

def event_list(request):
    # Imposta il filtro di default su IN_ATTESA se non specificato
    stato_filtro = request.GET.get('stato', 'IN_ATTESA')
    # Ottieni tutte le scelte possibili dallo stesso model
    scelte_stato = [s[0] for s in Evento._meta.get_field('stato').choices]
    if stato_filtro != 'TUTTI' and stato_filtro in scelte_stato:
        # Ordinamento crescente per data di inizio evento
        events = Evento.objects.filter(stato=stato_filtro).order_by('inizio_evento')
    else:
        # Ordinamento crescente per data di inizio evento
        events = Evento.objects.order_by('inizio_evento')

    # Paginazione
    paginator = Paginator(events, 9)  # 9 eventi per pagina
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    user = request.user
    is_direttivo = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Direttivo").exists())
    return render(request, 'lista_eventi.html', {
        'events': events,
        'is_direttivo': is_direttivo,
        'stato_filtro': stato_filtro,
        'scelte_stato': scelte_stato,
        'page_obj': events,
        'is_paginated': events.has_other_pages(),
    })

@login_required
def event_create(request):
    user = request.user
    is_direttivo = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Direttivo").exists())
    if not is_direttivo:
        return redirect('lista_eventi')
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Dopo il salvataggio, reindirizza SEMPRE alla lista eventi senza filtro stato
            return redirect('lista_eventi')
    else:
        form = EventoForm()
    return render(request, 'form_eventi.html', {'form': form, 'is_direttivo': is_direttivo})

def event_detail(request, pk):
    event = get_object_or_404(Evento, pk=pk)
    # Aggiorna lo stato in base ai posti disponibili ad ogni refresh
    stato_originale = event.stato
    if event.fine_evento and event.fine_evento < timezone.now():
        if event.stato != 'CONCLUSO':
            event.stato = 'CONCLUSO'
            event.save(update_fields=["stato"])
    elif event.posti_massimi and event.posti_disponibili() == 0 and event.stato not in ['CONCLUSO', 'ANNULLATO']:
        if event.stato != 'AL_COMPLETO':
            event.stato = 'AL_COMPLETO'
            event.save(update_fields=["stato"])
    elif event.stato == 'AL_COMPLETO' and (not event.posti_massimi or event.posti_disponibili() > 0):
        event.stato = 'IN_ATTESA'
        event.save(update_fields=["stato"])
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

    # Blocca la modifica di eventi conclusi (l'eliminazione rimane possibile)
    if event.stato == 'CONCLUSO':
        messages.error(request, 'Non è possibile modificare un evento concluso. L\'eliminazione rimane possibile dalla pagina di dettaglio.')
        return redirect('evento-detail', pk=event.pk)

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
