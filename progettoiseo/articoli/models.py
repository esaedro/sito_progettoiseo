from django.db import models
from progettoiseo.accounts.models import ProfiloUtente

# Create your models here.

class Articolo(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    titolo = models.CharField(max_length=200)
    testo = models.TextField(blank=False, null=False)
    autori = models.ManyToManyField(ProfiloUtente, related_name='articoli', db_table='articolo_autori')
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
    immagine = models.ImageField(upload_to='immagini_articoli/', blank=True, null=True)

    def __str__(self):
        return self.titolo

    class Meta:
        db_table = 'articoli'
        ordering = ['-data_pubblicazione']  # Ordina per data di pubblicazione decrescente
