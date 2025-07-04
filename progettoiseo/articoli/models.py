from django.db import models
from accounts.models import ProfiloUtente
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

# Create your models here.

class Articolo(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    titolo = models.CharField(max_length=200)
    testo = models.TextField(blank=False, null=False)
    autori = models.ManyToManyField(ProfiloUtente, related_name='articoli', db_table='articolo_autori')
    autori_eliminati = models.TextField(blank=True, help_text="Nomi degli autori eliminati, separati da virgola")
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
    immagine = models.ImageField(upload_to='immagini_articoli/', blank=True, null=True)

    def __str__(self):
        return self.titolo

    def get_tutti_autori(self):
        """Restituisce una lista con tutti gli autori (attivi ed eliminati)"""
        autori_attivi = [str(autore.user.get_full_name() or autore.user.username) for autore in self.autori.all()]
        autori_eliminati = []
        if self.autori_eliminati:
            autori_eliminati = [nome.strip() for nome in self.autori_eliminati.split(',') if nome.strip()]
        return autori_attivi + autori_eliminati

    def get_tags_list(self):
        if self.tag:
            # Estrai i tag usando solo # come delimitatore, mantenendo gli spazi interni, senza aggiungere #
            return [t.strip() for t in self.tag.split('#') if t.strip()]
        return []

    class Meta:
        db_table = 'articoli'
        ordering = ['-data_pubblicazione']  # Ordina per data di pubblicazione decrescente

    def delete(self, *args, **kwargs):
        # Elimina il file immagine associato, se presente
        if self.immagine and self.immagine.name:
            self.immagine.delete(save=False)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Se si sta aggiornando l'immagine, elimina il vecchio file
        if self.pk:
            try:
                old = Articolo.objects.get(pk=self.pk)
                if old.immagine and self.immagine and old.immagine != self.immagine:
                    old.immagine.delete(save=False)
            except Articolo.DoesNotExist:
                pass
        super().save(*args, **kwargs)


@receiver(m2m_changed, sender=Articolo.autori.through)
def preserva_autore_eliminato(sender, instance, action, pk_set, **kwargs):
    """Preserva i nomi degli autori quando vengono rimossi dalla relazione ManyToMany"""
    if action == "pre_remove" and pk_set:
        # Ottieni i nomi degli autori che stanno per essere rimossi
        autori_da_rimuovere = ProfiloUtente.objects.filter(pk__in=pk_set)
        nomi_da_preservare = []

        for autore in autori_da_rimuovere:
            nome = autore.user.get_full_name() or autore.user.username
            nomi_da_preservare.append(nome)

        # Aggiungi i nomi al campo autori_eliminati
        if nomi_da_preservare:
            if instance.autori_eliminati:
                # Se ci sono già autori eliminati, aggiungi i nuovi
                autori_esistenti = [nome.strip() for nome in instance.autori_eliminati.split(',') if nome.strip()]
                tutti_autori = list(set(autori_esistenti + nomi_da_preservare))  # Rimuovi duplicati
                instance.autori_eliminati = ', '.join(tutti_autori)
            else:
                # Se non ci sono autori eliminati, creane la lista
                instance.autori_eliminati = ', '.join(nomi_da_preservare)

            instance.save()
