from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ProfiloUtente

class ModificaPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class ModificaProfiloForm(forms.ModelForm):
    immagine_profilo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'}))
    email = forms.EmailField(required=True)
    numero_tessera = forms.CharField(max_length=20, required=False, disabled=True)
    data_tesseramento = forms.DateField(required=False, disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email if self.instance.user.email else ''
        
        # Aggiungi classi Bootstrap
        self.fields['immagine_profilo'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero_tessera'].widget.attrs.update({'class': 'form-control'})
        self.fields['data_tesseramento'].widget.attrs.update({'class': 'form-control', 'type': 'date'})

    def save(self, commit=True):
        profilo = super().save(commit=False)
        if self.cleaned_data['email']:
            profilo.user.email = self.cleaned_data['email']
            profilo.user.save()
        if commit:
            profilo.save()
        return profilo

    class Meta:
        model = ProfiloUtente
        fields = ['immagine_profilo', 'email', 'numero_tessera', 'data_tesseramento']

class RegistrazioneForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        label="Username o Email",
        help_text="Inserisci il tuo username o indirizzo email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
