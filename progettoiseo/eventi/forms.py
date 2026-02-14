import os
from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Case, IntegerField, When
from django.utils import timezone
from .models import Evento
from accounts.models import ProfiloUtente
from django.contrib.auth.models import Group
from progettoiseo.rich_text import sanitize_rich_text


class ClearableFileInputFilename(forms.ClearableFileInput):
    """ClearableFileInput che mostra solo il nome del file (senza percorso MEDIA)."""

    class _FileDisplay:
        def __init__(self, file):
            self._file = file
            self.name = getattr(file, "name", "")
            try:
                self.url = file.url
            except Exception:
                self.url = ""

        def __str__(self):
            return os.path.basename(self.name) if self.name else ""

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if context.get("widget", {}).get("is_initial") and value is not None and hasattr(value, "name"):
            context["widget"]["value"] = self._FileDisplay(value)
        return context

class EventoForm(forms.ModelForm):
    solo_data = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'role': 'switch',
                'id': 'solo-data',
            }
        ),
        label='Solo data',
    )

    class Meta:
        model = Evento
        fields = [
            'titolo', 'descrizione', 'inizio_evento', 'fine_evento',
            'solo_data',
            'luogo', 'immagine', 'posti_massimi', 'stato', 'organizzatore'
        ]
        widgets = {
            'titolo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': 'required'}),
            'inizio_evento': forms.DateTimeInput(
                attrs={'type': 'text', 'class': 'form-control', 'required': 'required', 'placeholder': 'Seleziona data e ora'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fine_evento': forms.DateTimeInput(
                attrs={'type': 'text', 'class': 'form-control', 'required': 'required', 'placeholder': 'Seleziona data e ora'},
                format='%Y-%m-%dT%H:%M'
            ),
            'luogo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'immagine': ClearableFileInputFilename(attrs={'class': 'form-control-file'}),
            'posti_massimi': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'}),
            'stato': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'organizzatore': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        # Sanitizza la descrizione (HTML da editor WYSIWYG)
        if 'descrizione' in cleaned_data:
            cleaned_data['descrizione'] = sanitize_rich_text(cleaned_data.get('descrizione', ''))

        # Durante la creazione, assicura che lo stato sia impostato a IN_ATTESA
        if not self.instance.pk:
            cleaned_data['stato'] = 'IN_ATTESA'

        if not cleaned_data.get('inizio_evento'):
            errors['inizio_evento'] = "Compila questo campo."
        if not cleaned_data.get('fine_evento'):
            errors['fine_evento'] = "Compila questo campo."
        if not cleaned_data.get('organizzatore'):
            errors['organizzatore'] = "Compila questo campo."

        # Supporto "solo data" (persistito su DB):
        # - se la checkbox è attiva (oppure arrivano YYYY-MM-DD), salva solo_data=True
        # - normalizza orari: inizio -> 00:00, fine -> 23:59
        raw_start = (self.data.get('inizio_evento') or '').strip()
        raw_end = (self.data.get('fine_evento') or '').strip()
        is_date_only_input = (raw_start and 'T' not in raw_start) or (raw_end and 'T' not in raw_end)
        solo_data = bool(cleaned_data.get('solo_data')) or is_date_only_input
        cleaned_data['solo_data'] = solo_data

        if solo_data and cleaned_data.get('inizio_evento') is not None:
            dt = cleaned_data['inizio_evento']
            cleaned_data['inizio_evento'] = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if solo_data and cleaned_data.get('fine_evento') is not None:
            dt = cleaned_data['fine_evento']
            cleaned_data['fine_evento'] = dt.replace(hour=23, minute=59, second=0, microsecond=0)

        # Validazione: fine >= inizio (dopo normalizzazione solo_data)
        start_dt = cleaned_data.get('inizio_evento')
        end_dt = cleaned_data.get('fine_evento')
        if start_dt is not None and end_dt is not None and end_dt < start_dt:
            errors['fine_evento'] = (
                "La data/ora di fine evento deve essere successiva o uguale a quella di inizio evento."
            )

        if errors:
            for field, msg in errors.items():
                self.add_error(field, msg)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Stato iniziale checkbox "Solo data" in modifica.
        if self.instance and getattr(self.instance, 'pk', None) and not self.is_bound:
            if getattr(self.instance, 'solo_data', False):
                self.fields['solo_data'].initial = True
            else:
                start = getattr(self.instance, 'inizio_evento', None)
                end = getattr(self.instance, 'fine_evento', None)
                inferred = bool(
                    start and end and start.hour == 0 and start.minute == 0 and end.hour == 23 and end.minute == 59
                )
                self.fields['solo_data'].initial = inferred

        # Non è più necessario cambiare il widget lato server: flatpickr gestisce tutto lato client
        # (Nel caso il form sia bound con errori, l'input rimane type=text e flatpickr lo gestisce correttamente)

        # L'organizzatore deve essere sempre selezionato: rimuove la scelta vuota "---------".
        self.fields['organizzatore'].required = True
        if hasattr(self.fields['organizzatore'], 'empty_label'):
            self.fields['organizzatore'].empty_label = None

        # Gestione dello stato in base a creazione/modifica
        is_creating = not self.instance.pk

        if is_creating:
            # Durante la creazione, nasconde il campo stato
            self.fields['stato'].widget = forms.HiddenInput()
            self.fields['stato'].initial = 'IN_ATTESA'
            # Default visualizzato nel form (creazione)
            self.fields['posti_massimi'].initial = 10

            # Default date/ora in creazione (solo se il form non è bound)
            # Scelta: domani 18:00 -> 20:00 per evitare 00:00 e date passate.
            if not self.is_bound:
                now_local = timezone.localtime(timezone.now())
                start_dt = (now_local + timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)
                end_dt = start_dt.replace(hour=20, minute=0)
                self.fields['inizio_evento'].initial = start_dt.strftime('%Y-%m-%dT%H:%M')
                self.fields['fine_evento'].initial = end_dt.strftime('%Y-%m-%dT%H:%M')
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
            base_qs = ProfiloUtente.objects.filter(
                Q(user__is_superuser=True) | Q(user__in=direttivo_users)
            ).exclude(user__username='admin')
        else:
            base_qs = ProfiloUtente.objects.filter(user__is_superuser=True).exclude(user__username='admin')

        # Aggiunge anche un'opzione fissa "Organizzazione Progetto Iseo" come primo elemento e default.
        org_profile = None
        try:
            UserModel = get_user_model()
            org_user, created = UserModel.objects.get_or_create(
                username='organizzazione_progetto_iseo',
                defaults={
                    'first_name': 'Direttivo',
                    'last_name': 'Progetto Iseo',
                    'is_active': True,
                },
            )
            if created:
                org_user.set_unusable_password()
                org_user.save(update_fields=['password'])
            else:
                # Se esiste già, assicura che il nome visualizzato sia coerente.
                changed = False
                if org_user.first_name != 'Direttivo':
                    org_user.first_name = 'Direttivo'
                    changed = True
                if org_user.last_name != 'Progetto Iseo':
                    org_user.last_name = 'Progetto Iseo'
                    changed = True
                if changed:
                    org_user.save(update_fields=['first_name', 'last_name'])

            org_profile = ProfiloUtente.objects.filter(user=org_user).first()
        except Exception:
            org_profile = None

        if org_profile is not None:
            qs = (ProfiloUtente.objects.filter(pk=org_profile.pk) | base_qs).distinct()
            qs = qs.annotate(
                _org_first=Case(
                    When(pk=org_profile.pk, then=0),
                    default=1,
                    output_field=IntegerField(),
                )
            ).order_by('_org_first', 'user__first_name', 'user__last_name', 'user__username')
            self.fields['organizzatore'].queryset = qs
            if is_creating and not self.is_bound:
                self.fields['organizzatore'].initial = org_profile.pk
        else:
            self.fields['organizzatore'].queryset = base_qs

        # Migliora la label
        self.fields['organizzatore'].label_from_instance = lambda obj: f"{obj.user.get_full_name() or obj.user.username}"

        # Fix visualizzazione valori precompilati per i campi datetime-local
        # + accetta anche formato solo data (YYYY-MM-DD)
        for field in ['inizio_evento', 'fine_evento']:
            if hasattr(self.fields.get(field), 'input_formats'):
                # aggiunge senza perdere i default di Django
                current = list(self.fields[field].input_formats or [])
                # Formati supportati: ISO datetime con T, ISO date solo, e altri comuni
                formats_to_add = [
                    '%Y-%m-%dT%H:%M',       # 2026-02-14T18:00
                    '%Y-%m-%d %H:%M',       # 2026-02-14 18:00
                    '%Y-%m-%dT%H:%M:%S',    # 2026-02-14T18:00:00
                    '%Y-%m-%d',             # 2026-02-14
                ]
                for fmt in formats_to_add:
                    if fmt not in current:
                        current.insert(0, fmt)
                self.fields[field].input_formats = current

        for field in ['inizio_evento', 'fine_evento']:
            if self.instance and getattr(self.instance, field):
                value = getattr(self.instance, field)
                self.fields[field].initial = value.strftime('%Y-%m-%dT%H:%M')
