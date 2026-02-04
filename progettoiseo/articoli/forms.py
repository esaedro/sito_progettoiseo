import os

from django import forms
from .models import Articolo
from accounts.models import ProfiloUtente
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

class InserimentoArticoloForm(forms.ModelForm):
    titolo = forms.CharField(
        label="Titolo",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Inserisci il titolo dell'articolo.",
    )
    
    autori = forms.ModelMultipleChoiceField(
        queryset=ProfiloUtente.objects.all(),
        label="Autori",
        widget=forms.CheckboxSelectMultiple,
        help_text="Seleziona gli autori dell'articolo.",
        required=False
    )

    a_nome_organizzazione = forms.BooleanField(
        label="A nome dell'organizzazione",
        required=False,
        initial=False,
        help_text="Se selezionato, l'articolo risulterà pubblicato a nome dell'organizzazione.",
    )

    tag = forms.CharField(
        label="Tag",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Inserisci i tag dell'articolo, separati da spazio.",
    )
    immagine = forms.ImageField(
        label="Immagine",
        required=False,
        widget=ClearableFileInputFilename(attrs={'class': 'form-control-file'}),
        help_text="Carica un'immagine per l'articolo (opzionale).",
    )
    testo = forms.CharField(
        label="Testo",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        help_text="Inserisci il testo dell'articolo.",
    ) 


    def __init__(self, *args, user=None, **kwargs):    
        super().__init__(*args, **kwargs)
        self.user = user
        # Filtra gli autori: solo membri del gruppo Direttivo
        from django.contrib.auth.models import Group
        try:
            gruppo_direttivo = Group.objects.get(name='Direttivo')
            direttivo_users = gruppo_direttivo.user_set.all()
            self.fields['autori'].queryset = ProfiloUtente.objects.filter(user__in=direttivo_users)
        except Group.DoesNotExist:
            self.fields['autori'].queryset = ProfiloUtente.objects.none()
        self.fields['autori'].label_from_instance = lambda obj: f"{obj.user.get_full_name() or obj.user.username}"

        # Se l'istanza esiste, preseleziona i valori correnti
        if self.instance and self.instance.pk:
            self.fields['autori'].initial = self.instance.autori.all()
            self.fields['titolo'].initial = self.instance.titolo
            # Se non ci sono autori selezionati, l'articolo è a nome dell'organizzazione
            # (imposta solo se il form non è bound, per non sovrascrivere input utente dopo errori)
            if not self.is_bound:
                self.fields['a_nome_organizzazione'].initial = (not self.instance.autori.exists())
            # Ricostruisci la stringa dei tag come erano stati inseriti, usando solo # come delimitatore
            if self.instance.tag:
                tag_list = [f'#{t.strip()}' for t in self.instance.tag.split('#') if t.strip()]
                self.fields['tag'].initial = ' '.join(tag_list)
            else:
                self.fields['tag'].initial = ''
            self.fields['immagine'].initial = self.instance.immagine
            self.fields['testo'].initial = self.instance.testo
        else:
            # In creazione: seleziona di default "a nome dell'organizzazione"
            # (solo se il form non è bound, per non sovrascrivere input utente dopo errori)
            if not self.is_bound:
                self.fields['a_nome_organizzazione'].initial = True
        
        # Aggiungi classi CSS per migliorare l'aspetto del form
        self.fields['titolo'].widget.attrs.update({'class': 'form-control'})
        self.fields['autori'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['a_nome_organizzazione'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['tag'].widget.attrs.update({'class': 'form-control'})
        self.fields['immagine'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['testo'].widget.attrs.update({'class': 'form-control', 'rows': 5})

    def clean(self):
        cleaned_data = super().clean()
        autori = cleaned_data.get('autori')

        # Mutua esclusività:
        # - se è selezionato "a nome dell'organizzazione", questa scelta ha priorità e ignora eventuali autori
        # - altrimenti, se è selezionato un autore, "a nome dell'organizzazione" deve risultare deselezionato
        if cleaned_data.get('a_nome_organizzazione'):
            cleaned_data['autori'] = ProfiloUtente.objects.none()
        elif autori is not None and autori.exists():
            cleaned_data['a_nome_organizzazione'] = False

        # Obbligatorietà: deve esserci almeno un autore, oppure "a nome dell'organizzazione".
        autori_final = cleaned_data.get('autori')
        if not cleaned_data.get('a_nome_organizzazione'):
            if autori_final is None or not autori_final.exists():
                self.add_error('autori', 'Seleziona almeno un autore oppure scegli "A nome dell\'organizzazione".')

        return cleaned_data

    def save(self, commit=True):
        articolo = super().save(commit=False)
        if self.cleaned_data['titolo']:
            articolo.titolo = self.cleaned_data['titolo']
        if self.cleaned_data['tag']:
            tag_string = self.cleaned_data['tag']
            # Estrai i tag usando # come delimitatore; rimuove duplicati in modo case-insensitive
            unique_by_lower = {}
            for raw in tag_string.split('#'):
                t = raw.strip()
                if not t:
                    continue
                key = t.lower()
                if key not in unique_by_lower:
                    unique_by_lower[key] = t
            articolo.tag = ' '.join([f'#{t}' for t in unique_by_lower.values()])
        if self.cleaned_data['immagine']:
            articolo.immagine = self.cleaned_data['immagine']
        if self.cleaned_data.get('testo') is not None:
            articolo.testo = sanitize_rich_text(self.cleaned_data.get('testo', ''))
        articolo.save()  # Salva sempre prima di gestire M2M

        # Gestione autori
        # Se selezionato "a nome dell'organizzazione", non impostare autori personali.
        if self.cleaned_data.get('a_nome_organizzazione'):
            articolo.autori.set([])
            # In modalità "organizzazione" non devono comparire autori precedenti nel dettaglio.
            # Il signal m2m_changed può salvare i nomi rimossi in autori_eliminati: li azzeriamo.
            if articolo.autori_eliminati:
                articolo.autori_eliminati = ''
                articolo.save(update_fields=['autori_eliminati'])
        else:
            # Salva solo gli autori selezionati manualmente
            autori = list(self.cleaned_data.get('autori', [])) if self.cleaned_data.get('autori') else []
            articolo.autori.set(autori)

        return articolo
    
    class Meta:
        model = Articolo
        fields = ['titolo', 'autori', 'tag', 'immagine', 'testo']
