from django.db import models
from django.db.models import signals as receivers
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, pre_delete, pre_save
from accounts.models import ProfiloUtente
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

@receiver(receivers.pre_save, sender=Evento)
def validate_evento_fields(sender, instance, **kwargs):
    """
    Validazione dei campi dell'evento prima del salvataggio.
    """ 
    if not instance.titolo:
        raise ValueError("Il titolo dell'evento non può essere vuoto.")
    if not instance.descrizione:
        raise ValueError("La descrizione dell'evento non può essere vuota.")
    if not instance.luogo:
        raise ValueError("Il luogo dell'evento non può essere vuoto.")
    if not instance.date_evento:
        raise ValueError("La data dell'evento non può essere vuota.")
    if instance.stato not in dict(Evento._meta.get_field('stato').choices):
        raise ValueError(f"Stato dell'evento non valido: {instance.stato}") 


    """    Validazione dei campi dell'evento prima del salvataggio.
    Assicurati che il titolo, la descrizione, il luogo e la data siano forniti. 
    Controlla che lo stato sia uno dei valori consentiti.
    """
    if not isinstance(instance.date_evento, list):
        raise ValueError("La data dell'evento deve essere una lista di stringhe.")
    for date in instance.date_evento:
        if not isinstance(date, str):
            raise ValueError("Ogni data dell'evento deve essere una stringa.")
        # Puoi aggiungere ulteriori validazioni per il formato della data qui, se necessario
    if instance.immagine and not instance.immagine.name.endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError("L'immagine dell'evento deve essere in formato PNG, JPG o JPEG.")      
    if instance.organizzatore is None:
        raise ValueError("L'organizzatore dell'evento non può essere vuoto.")
    if instance.numero_partecipanti < 0:
        raise ValueError("Il numero di partecipanti non può essere negativo.")
    # Aggiungi altre validazioni specifiche per il tuo modello se necessario
    # Se tutte le validazioni passano, il modello può essere salvato
    # Se tutte le validazioni passano, il modello può essere salvato


@receiver(receivers.post_save, sender=Evento)
def create_evento(sender, instance, created, **kwargs):
    """
    Crea un nuovo evento e inizializza il numero di partecipanti.
    """
    if created:
        instance.numero_partecipanti = instance.iscritti.count()
        instance.save()
        print(f"Evento creato: {instance.titolo} da {instance.organizzatore.username}")
    else:
        print(f"Evento aggiornato: {instance.titolo} da {instance.organizzatore.username}") 

@receiver(post_save, sender=Evento)
def update_evento(sender, instance, created, **kwargs):
    """
    Aggiorna l'evento quando viene creato o modificato.
    """
    if created:
        instance.numero_partecipanti = instance.iscritti.count()
        instance.save()
        print(f"Evento creato: {instance.titolo} da {instance.organizzatore.username}")
    else:
        print(f"Evento aggiornato: {instance.titolo} da {instance.organizzatore.username}")


@receiver(receivers.m2m_changed, sender=Evento.iscritti.through)
def m2m_evento_iscritti(sender, instance, action, **kwargs):


    """
    Gestisce i cambiamenti nella relazione molti-a-molti tra Evento e Utente.
    Aggiorna il numero di partecipanti all'evento quando gli iscritti cambiano.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.numero_partecipanti = instance.iscritti.count()
        instance.save()
        print(f"Numero di partecipanti aggiornato per l'evento: {instance.titolo} - {instance.numero_partecipanti} iscritti")


@receivers.post_save(sender=Evento)
def update_evento_count(sender, instance, created, **kwargs):
    """
    Aggiorna il numero di partecipanti all'evento quando un utente si iscrive o disiscrive.
    """
    if created:
        instance.numero_partecipanti = instance.iscritti.count()
        instance.save()
    else:
        instance.numero_partecipanti = instance.iscritti.count()
        instance.save()


@receiver(receivers.m2m_changed, sender=Evento.iscritti.through)
def update_evento_iscritti(sender, instance, action, **kwargs):
    """
    Aggiorna il numero di partecipanti all'evento quando gli iscritti cambiano.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.numero_partecipanti = instance.iscritti.count()
        instance.save()

@receiver(receivers.pre_delete, sender=Evento) 
def delete_evento_image(sender, instance, **kwargs):
    """
    Elimina l'immagine dell'evento quando l'evento viene cancellato.
    """
    if instance.immagine:
        instance.immagine.delete(save=False)

@receiver(receivers.pre_save, sender=Evento)
def validate_event_date(sender, instance, **kwargs):
    """
    Validazione della data dell'evento.
    """
    if not instance.date_evento:
        raise ValueError("La data dell'evento non può essere vuota.")
    
    # Assicurati che la data sia in un formato valido
    for date in instance.date_evento:
        if not isinstance(date, str):
            raise ValueError("La data dell'evento deve essere una stringa.")
        
    # Puoi aggiungere ulteriori validazioni qui, ad esempio controllare che la data non sia nel passato
@receiver(receivers.post_save, sender=Evento)
def notify_event_creation(sender, instance, created, **kwargs):
    """
    Notifica la creazione di un nuovo evento.
    """
    if created:
        # Logica per inviare una notifica o un'email all'organizzatore
        print(f"Evento creato: {instance.titolo} da {instance.organizzatore.username}")
        # Qui puoi integrare un sistema di notifica o email
 


@receiver(receivers.post_delete, sender=Evento)
def notify_event_deletion(sender, instance, **kwargs):
    """
    Notifica la cancellazione di un evento.
    """
    # Logica per inviare una notifica o un'email all'organizzatore
    print(f"Evento cancellato: {instance.titolo} da {instance.organizzatore.username}")

