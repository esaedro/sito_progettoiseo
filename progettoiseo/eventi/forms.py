from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titolo', 'descrizione', 'inizio_evento', 'fine_evento', 'luogo', 'immagine', 'posti_massimi', 'stato', 'organizzatore']
        widgets = {
            'inizio_evento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fine_evento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
