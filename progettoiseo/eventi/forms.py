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

        # Durante la creazione, assicura che lo stato sia impostato a IN_ATTESA
        if not self.instance.pk:
            cleaned_data['stato'] = 'IN_ATTESA'

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

        # Gestione dello stato in base a creazione/modifica
        is_creating = not self.instance.pk

        if is_creating:
            # Durante la creazione, nasconde il campo stato
            self.fields['stato'].widget = forms.HiddenInput()
            self.fields['stato'].initial = 'IN_ATTESA'
        else:
            # Durante la modifica, gestisce le scelte in base allo stato attuale
            if self.instance.stato == 'IN_ATTESA':
                # Da IN_ATTESA può andare solo ad ANNULLATO
                available_choices = [
                    ('IN_ATTESA', 'IN_ATTESA'),
                    ('ANNULLATO', 'ANNULLATO')
                ]
            elif self.instance.stato == 'AL_COMPLETO':
                # Da AL_COMPLETO può andare solo ad ANNULLATO
                available_choices = [
                    ('AL_COMPLETO', 'AL_COMPLETO'),
                    ('ANNULLATO', 'ANNULLATO')
                ]
            elif self.instance.stato == 'ANNULLATO':
                # Da ANNULLATO può tornare solo a IN_ATTESA
                available_choices = [
                    ('IN_ATTESA', 'IN_ATTESA'),
                    ('ANNULLATO', 'ANNULLATO')
                ]
            else:
                # CONCLUSO - questo caso non dovrebbe mai verificarsi
                # perché la view blocca la modifica di eventi conclusi
                available_choices = [
                    ('IN_ATTESA', 'IN_ATTESA'),
                    ('ANNULLATO', 'ANNULLATO')
                ]

            self.fields['stato'].choices = available_choices

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
