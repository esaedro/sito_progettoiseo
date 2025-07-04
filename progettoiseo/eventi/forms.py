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
            'titolo': forms.TextInput(attrs={'class': 'form-control'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'inizio_evento': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fine_evento': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'luogo': forms.TextInput(attrs={'class': 'form-control'}),
            'immagine': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'posti_massimi': forms.NumberInput(attrs={'class': 'form-control'}),
            'stato': forms.Select(attrs={'class': 'form-select'}),
            'organizzatore': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra solo superuser e membri del direttivo come organizzatori
        direttivo = Group.objects.filter(name='Direttivo').first()
        if direttivo:
            direttivo_users = direttivo.user_set.all()
            self.fields['organizzatore'].queryset = ProfiloUtente.objects.filter(
                Q(user__is_superuser=True) | Q(user__in=direttivo_users)
            )
        else:
            self.fields['organizzatore'].queryset = ProfiloUtente.objects.filter(user__is_superuser=True)
        # Migliora la label
        self.fields['organizzatore'].label_from_instance = lambda obj: f"{obj.user.get_full_name() or obj.user.username}"

        # Fix visualizzazione valori precompilati per i campi datetime-local
        for field in ['inizio_evento', 'fine_evento']:
            if self.instance and getattr(self.instance, field):
                value = getattr(self.instance, field)
                self.fields[field].initial = value.strftime('%Y-%m-%dT%H:%M')
