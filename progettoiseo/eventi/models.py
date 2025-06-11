from django.db import models
from progettoiseo.accounts.models import ProfiloUtente

# Create your models here.

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField(blank=False, null=False)
    date_evento = models.JSONField(default=list)
    luogo = models.CharField(max_length=255, blank=False, null=False)
    immagine = models.ImageField(upload_to='immagini_eventi/', blank=True, null=True)
    numero_partecipanti = models.PositiveIntegerField(default=0, blank=True, null=True)
    stato = models.CharField(max_length=50, choices=[('IN_ATTESA', 'IN_ATTESA'), ('CONCLUSO', 'CONCLUSO'), ('AL_COMPLETO', 'AL_COMPLETO'), ('ANNULLATO', 'ANNULLATO')], default='IN_ATTESA')
    organizzatore = models.ForeignKey(ProfiloUtente, on_delete=models.SET_NULL, related_name='eventi_organizzati', db_column='organizzatore_id', null=True, blank=True)
    iscritti = models.ManyToManyField(ProfiloUtente, related_name='eventi_iscritti', blank=True, db_table='evento_iscritti')

    def __str__(self):
        return str(self.titolo)

    class Meta:
        db_table = 'eventi'
        ordering = [models.F('date_evento').desc()]  # Ordina per la prima data della lista in ordine decrescente
