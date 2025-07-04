from django import forms
from .models import Articolo
from accounts.models import ProfiloUtente

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
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
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
            # Ricostruisci la stringa dei tag come erano stati inseriti, usando solo # come delimitatore
            if self.instance.tag:
                tag_list = [f'#{t.strip()}' for t in self.instance.tag.split('#') if t.strip()]
                self.fields['tag'].initial = ' '.join(tag_list)
            else:
                self.fields['tag'].initial = ''
            self.fields['immagine'].initial = self.instance.immagine
            self.fields['testo'].initial = self.instance.testo
        
        # Aggiungi classi CSS per migliorare l'aspetto del form
        self.fields['titolo'].widget.attrs.update({'class': 'form-control'})
        self.fields['autori'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['tag'].widget.attrs.update({'class': 'form-control'})
        self.fields['immagine'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['testo'].widget.attrs.update({'class': 'form-control', 'rows': 5})

    def save(self, commit=True):
        articolo = super().save(commit=False)
        if self.cleaned_data['titolo']:
            articolo.titolo = self.cleaned_data['titolo']
        if self.cleaned_data['tag']:
            tag_string = self.cleaned_data['tag']
            # Estrai i tag usando solo # come delimitatore, mantenendo gli spazi interni
            tag_list = [f'#{t.strip()}' for t in tag_string.split('#') if t.strip()]
            articolo.tag = ' '.join(tag_list)
        if self.cleaned_data['immagine']:
            articolo.immagine = self.cleaned_data['immagine']
        if self.cleaned_data['testo']:
            articolo.testo = self.cleaned_data['testo']
        articolo.save()  # Salva sempre prima di gestire M2M

        # Gestione autori: prendi quelli selezionati e aggiungi sempre l'utente corrente
        autori = list(self.cleaned_data.get('autori', [])) if self.cleaned_data.get('autori') else []
        if self.user is not None:
            profilo_utente, _ = ProfiloUtente.objects.get_or_create(user=self.user)
            if profilo_utente not in autori:
                autori.append(profilo_utente)
        articolo.autori.set(autori)

        return articolo
    
    class Meta:
        model = Articolo
        fields = ['titolo', 'autori', 'tag', 'immagine', 'testo']

#TODO- DONE?: L'utente che sta creando l'articolo dovrebbe essere automaticamente aggiunto come autore
#Inoltre la lista degli autori selezionabili deve contenere solo membri del direttivo
#e non tutti gli utenti registrati. Per fare questo, si può filtrare il queryset