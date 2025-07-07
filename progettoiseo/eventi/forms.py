from django import forms
from django.db.models import Q
from .models import Evento
from accounts.models import ProfiloUtente
from django.contrib.auth.models import Group

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'titolo', 'descrizione', 'inizio_evento', 'fine_evento',
            'luogo', 'immagine', 'posti_massimi', 'stato', 'organizzatore'
        ]
        widgets = {
            'titolo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': 'required'}),
            'inizio_evento': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'required': 'required'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fine_evento': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'required': 'required'},
                format='%Y-%m-%dT%H:%M'
            ),
            'luogo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'immagine': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'posti_massimi': forms.NumberInput(attrs={'class': 'form-control'}),
            'stato': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'organizzatore': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        errors = {}
        if not cleaned_data.get('inizio_evento'):
            errors['inizio_evento'] = "Compila questo campo."
        if not cleaned_data.get('fine_evento'):
            errors['fine_evento'] = "Compila questo campo."
        if not cleaned_data.get('organizzatore'):
            errors['organizzatore'] = "Compila questo campo."
        if errors:
            for field, msg in errors.items():
                self.add_error(field, msg)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra solo superuser e membri del direttivo come organizzatori
        direttivo = Group.objects.filter(name='Direttivo').first()
        if direttivo:
            direttivo_users = direttivo.user_set.exclude(username='admin')
            self.fields['organizzatore'].queryset = ProfiloUtente.objects.filter(
                Q(user__is_superuser=True) | Q(user__in=direttivo_users)
            ).exclude(user__username='admin')
        else:
            self.fields['organizzatore'].queryset = ProfiloUtente.objects.filter(user__is_superuser=True).exclude(user__username='admin')
        # Migliora la label
        self.fields['organizzatore'].label_from_instance = lambda obj: f"{obj.user.get_full_name() or obj.user.username}"

        # Fix visualizzazione valori precompilati per i campi datetime-local
        for field in ['inizio_evento', 'fine_evento']:
            if self.instance and getattr(self.instance, field):
                value = getattr(self.instance, field)
                self.fields[field].initial = value.strftime('%Y-%m-%dT%H:%M')
