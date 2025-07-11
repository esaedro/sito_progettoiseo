from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import LoginForm, ModificaProfiloForm, ModificaPasswordForm, RegistrazioneForm
from .models import ProfiloUtente
# Create your views here.

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Prova autenticazione con backend personalizzato
            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                if password.startswith("##"):
                    messages.success(request, 'Cambia la password provvisoria')
                    return redirect('modifica-password')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Username/Email o password non corretti.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logout effettuato con successo.')
        return redirect('logout_success')
    else:
        # Se è una GET request, mostra una pagina di conferma
        return render(request, 'registration/logout_confirm.html')

def logout_success(request):
    return render(request, 'registration/logout.html')

@permission_required('accounts.add_profiloutente')
def registrazione(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            user = form.save() # Il signal di ProfiloUtente si occupa di creare e inizializzare automaticamente il profilo

            messages.success(request, f'Registrazione di {user.username} completata con successo!')
            return redirect('registrazione')
        else:
            messages.error(request, 'Ci sono errori nel form. Controlla i dati inseriti.')
    else:
        form = RegistrazioneForm()
    return render(request, 'registrazione.html', {'form': form})

@login_required
def modifica_profilo(request):
    profilo_utente, created = ProfiloUtente.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ModificaProfiloForm(request.POST, request.FILES, instance=profilo_utente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('profilo')
        else:
            print(f"Errori form: {form.errors}")  # DEBUG
    else:
        form = ModificaProfiloForm(instance=profilo_utente)
    return render(request, 'profilo.html', {'form': form, 'profilo_utente': profilo_utente})

@login_required
def modifica_password(request):
    if request.method == 'POST':
        form = ModificaPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantieni l'utente loggato dopo il cambio password
            update_session_auth_hash(request, user)
            messages.success(request, 'Password modificata con successo!')
            return redirect('profilo')
        else:
            messages.error(request, 'Errore nella modifica della password. Controlla i dati inseriti.')
    else:
        form = ModificaPasswordForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})

@login_required
@require_POST
def rimuovi_foto_profilo(request):
    try:
        profilo_utente = ProfiloUtente.objects.get(user=request.user)
        if profilo_utente.immagine_profilo:
            # Elimina il file fisico
            profilo_utente.immagine_profilo.delete(save=False)
            # Rimuovi il riferimento dal database
            profilo_utente.immagine_profilo = None
            profilo_utente.save()

            return JsonResponse({
                'success': True,
                'message': 'Foto profilo rimossa con successo!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Nessuna foto profilo da rimuovere.'
            })
    except ProfiloUtente.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Profilo utente non trovato.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Errore durante la rimozione: {str(e)}'
        })
