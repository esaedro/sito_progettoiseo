from django.db import models
from django.db.models import signals as receivers
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, pre_delete, pre_save
from django.utils import timezone
from accounts.models import ProfiloUtente
# Create your models here.

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField(blank=False, null=False)
    inizio_evento = models.DateTimeField(null=True, blank=True)
    fine_evento = models.DateTimeField(null=True, blank=True)
    luogo = models.CharField(max_length=255, blank=False, null=False)
    immagine = models.ImageField(upload_to='immagini_eventi/', blank=True, null=True)
    numero_partecipanti = models.PositiveIntegerField(default=0, blank=True, null=True)
    posti_massimi = models.PositiveIntegerField(default=0, blank=True, null=True)
    stato = models.CharField(max_length=50, choices=[('IN_ATTESA', 'IN_ATTESA'), ('CONCLUSO', 'CONCLUSO'), ('AL_COMPLETO', 'AL_COMPLETO'), ('ANNULLATO', 'ANNULLATO')], default='IN_ATTESA')
    organizzatore = models.ForeignKey(ProfiloUtente, on_delete=models.SET_NULL, related_name='eventi_organizzati', db_column='organizzatore_id', null=True, blank=True)
    iscritti = models.ManyToManyField(ProfiloUtente, related_name='eventi_iscritti', blank=True, db_table='evento_iscritti')

    def posti_disponibili(self):
        if self.posti_massimi:
            return max(self.posti_massimi - self.numero_partecipanti, 0)
        return None

    def is_iscrivibile(self):
        return self.posti_disponibili() is None or self.posti_disponibili() > 0

    def __str__(self):
        return str(self.titolo)

    class Meta:
        db_table = 'eventi'
        ordering = ['-inizio_evento']

    def save(self, *args, **kwargs):
        # Aggiorna stato a CONCLUSO se la data di fine è passata
        if self.fine_evento and self.fine_evento < timezone.now():
            self.stato = 'CONCLUSO'
        # Aggiorna stato a AL_COMPLETO se i posti sono finiti (solo se non già concluso o annullato)
        elif self.posti_massimi and self.posti_disponibili() == 0 and self.stato not in ['CONCLUSO', 'ANNULLATO']:
            self.stato = 'AL_COMPLETO'
        super().save(*args, **kwargs)

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
    if not instance.inizio_evento or not instance.fine_evento:
        raise ValueError("Le date di inizio e fine dell'evento non possono essere vuote.")
    if instance.stato not in dict(Evento._meta.get_field('stato').choices):
        raise ValueError(f"Stato dell'evento non valido: {instance.stato}")
    if instance.immagine and not instance.immagine.name.endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError("L'immagine dell'evento deve essere in formato PNG, JPG o JPEG.")
    if instance.organizzatore is None:
        raise ValueError("L'organizzatore dell'evento non può essere vuoto.")
    if instance.numero_partecipanti < 0:
        raise ValueError("Il numero di partecipanti non può essere negativo.")
    # Puoi aggiungere ulteriori validazioni qui, ad esempio controllare che la data non sia nel passato
    if instance.inizio_evento and instance.fine_evento:
        if instance.fine_evento < instance.inizio_evento:
            raise ValueError("La data di fine evento non può essere precedente a quella di inizio.")

@receiver(receivers.post_save, sender=Evento)
def create_evento(sender, instance, created, **kwargs):
    """
    Crea un nuovo evento e stampa info (senza richiamare save per evitare ricorsione).
    """
    if created:
        if instance.organizzatore and hasattr(instance.organizzatore, 'utente'):
            print(f"Evento creato: {instance.titolo} da {instance.organizzatore.utente.username}")
        else:
            print(f"Evento creato: {instance.titolo}")
    else:
        if instance.organizzatore and hasattr(instance.organizzatore, 'utente'):
            print(f"Evento aggiornato: {instance.titolo} da {instance.organizzatore.utente.username}")
        else:
            print(f"Evento aggiornato: {instance.titolo}")

@receiver(receivers.m2m_changed, sender=Evento.iscritti.through)
def m2m_evento_iscritti(sender, instance, action, **kwargs):
    """
    Gestisce i cambiamenti nella relazione molti-a-molti tra Evento e Utente.
    Aggiorna il numero di partecipanti all'evento quando gli iscritti cambiano.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.numero_partecipanti = instance.iscritti.count()
        instance.save(update_fields=["numero_partecipanti"])
        if instance.organizzatore and hasattr(instance.organizzatore, 'utente'):
            print(f"Numero di partecipanti aggiornato per l'evento: {instance.titolo} - {instance.numero_partecipanti} iscritti (organizzatore: {instance.organizzatore.utente.username})")
        else:
            print(f"Numero di partecipanti aggiornato per l'evento: {instance.titolo} - {instance.numero_partecipanti} iscritti")


@receiver(receivers.pre_delete, sender=Evento)
def delete_evento_image(sender, instance, **kwargs):
    """
    Elimina l'immagine dell'evento quando l'evento viene cancellato.
    """
    if instance.immagine:
        instance.immagine.delete(save=False)

@receiver(receivers.post_save, sender=Evento)
def notify_event_creation(sender, instance, created, **kwargs):
    """
    Notifica la creazione di un nuovo evento.
    """
    if created:
        if instance.organizzatore and hasattr(instance.organizzatore, 'utente'):
            print(f"Evento creato: {instance.titolo} da {instance.organizzatore.utente.username}")
        else:
            print(f"Evento creato: {instance.titolo}")
        # Qui puoi integrare un sistema di notifica o email



@receiver(receivers.post_delete, sender=Evento)
def notify_event_deletion(sender, instance, **kwargs):
    """
    Notifica la cancellazione di un evento.
    """
    if instance.organizzatore and hasattr(instance.organizzatore, 'utente'):
        print(f"Evento cancellato: {instance.titolo} da {instance.organizzatore.utente.username}")
    else:
        print(f"Evento cancellato: {instance.titolo}")

@receiver(receivers.pre_save, sender=Evento)
def validate_event_date(sender, instance, **kwargs):
    """
    Validazione della data dell'evento.
    """
    if not instance.inizio_evento or not instance.fine_evento:
        raise ValueError("Le date di inizio e fine dell'evento non possono essere vuote.")
    # Assicurati che la data di fine sia successiva o uguale a quella di inizio
    if instance.fine_evento < instance.inizio_evento:
        raise ValueError("La data/ora di fine evento deve essere successiva o uguale a quella di inizio evento.")