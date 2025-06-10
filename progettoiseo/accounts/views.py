from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import ModificaProfiloForm, ModificaPasswordForm, RegistrazioneForm, LoginForm
from django.shortcuts import redirect
from django.contrib import messages
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
        return render(request, 'registration/logout.html')
    else:
        # Se è una GET request, mostra una pagina di conferma
        return render(request, 'registration/logout_confirm.html')

def registrazione(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(f"Errori form: {form.errors}")  # DEBUG
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
            return redirect('profilo')
        else:
            print(f"Errori form: {form.errors}")  # DEBUG
    else:
        form = ModificaProfiloForm(instance=profilo_utente)
    return render(request, 'profilo.html', {'form': form, 'profilo_utente': profilo_utente})

@login_required
def form_modifica_password(request):
    if request.method == 'POST':
        form = ModificaPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('profilo')
    else:
        form = ModificaPasswordForm(request.user)
    return render(request, 'modifica_password.html', {'form': form})
