from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ProfiloUtente
from calendar import firstweekday

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
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    immagine_profilo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'}))
    email = forms.EmailField(required=False)
    numero_tessera = forms.CharField(max_length=20, required=True, disabled=True)
    data_tesseramento = forms.DateField(required=True, disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email if self.instance.user.email else ''
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        # Aggiungi classi Bootstrap
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['immagine_profilo'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero_tessera'].widget.attrs.update({'class': 'form-control'})
        self.fields['data_tesseramento'].widget.attrs.update({'class': 'form-control', 'type': 'date'})



    def save(self, commit=True):
        profilo = super().save(commit=False)
        if self.cleaned_data['email']:
            profilo.user.email = self.cleaned_data['email']
        if self.cleaned_data['username']:
            profilo.user.username = self.cleaned_data['username']
        if self.cleaned_data['first_name']:
            profilo.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            profilo.user.last_name = self.cleaned_data['last_name']
        profilo.user.save()



        if commit:
            profilo.save()
        return profilo

    class Meta:
        model = ProfiloUtente
        fields = ['username', 'immagine_profilo', 'email', 'numero_tessera', 'data_tesseramento']

class RegistrazioneForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            if User.objects.filter(email=username).exists():
                raise forms.ValidationError("Questa email è già registrata.")
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError("Questo username è già registrato.")
        return username


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
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
