from django.db import models
from django.db.models import signals as receivers
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import ProfiloUtente
# Create your models here.

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField(blank=False, null=False)
    inizio_evento = models.DateTimeField(null=True, blank=True)
    fine_evento = models.DateTimeField(null=True, blank=True)
    solo_data = models.BooleanField(default=False)
    luogo = models.CharField(max_length=255, blank=False, null=False)
    immagine = models.ImageField(upload_to='eventi/', blank=True, null=True)
    numero_partecipanti = models.PositiveIntegerField(default=0, blank=True, null=True)
    posti_massimi = models.PositiveIntegerField(default=10, blank=True, null=True)
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

    def clean(self):
        errors = {}

        if not self.titolo:
            errors['titolo'] = "Il titolo dell'evento non può essere vuoto."
        if not self.descrizione:
            errors['descrizione'] = "La descrizione dell'evento non può essere vuota."
        if not self.luogo:
            errors['luogo'] = "Il luogo dell'evento non può essere vuoto."
        if not self.inizio_evento:
            errors['inizio_evento'] = "Compila questo campo."
        if not self.fine_evento:
            errors['fine_evento'] = "Compila questo campo."

        if self.stato and self.stato not in dict(self._meta.get_field('stato').choices):
            errors['stato'] = f"Stato dell'evento non valido: {self.stato}"

        if self.immagine and getattr(self.immagine, 'name', '') and not self.immagine.name.lower().endswith(
            ('.png', '.jpg', '.jpeg')
        ):
            errors['immagine'] = "L'immagine dell'evento deve essere in formato PNG, JPG o JPEG."

        if self.organizzatore is None:
            errors['organizzatore'] = "L'organizzatore dell'evento non può essere vuoto."

        if self.numero_partecipanti is not None and self.numero_partecipanti < 0:
            errors['numero_partecipanti'] = "Il numero di partecipanti non può essere negativo."

        if self.inizio_evento and self.fine_evento:
            start = self.inizio_evento
            end = self.fine_evento

            # Normalizza aware/naive per evitare TypeError in confronto.
            tz = timezone.get_current_timezone()
            if timezone.is_aware(start) and timezone.is_naive(end):
                end = timezone.make_aware(end, tz)
            elif timezone.is_naive(start) and timezone.is_aware(end):
                start = timezone.make_aware(start, tz)

            if end < start:
                errors['fine_evento'] = (
                    "La data/ora di fine evento deve essere successiva o uguale a quella di inizio evento."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Valida sempre il model (anche quando si salva fuori da ModelForm)
        self.full_clean()

        # Aggiorna stato a CONCLUSO se la data di fine è passata
        if self.fine_evento and self.fine_evento < timezone.now():
            self.stato = 'CONCLUSO'
        # Aggiorna stato a AL_COMPLETO se i posti sono finiti (solo se non già concluso o annullato)
        elif self.posti_massimi and self.posti_disponibili() == 0 and self.stato not in ['CONCLUSO', 'ANNULLATO']:
            self.stato = 'AL_COMPLETO'
        super().save(*args, **kwargs)

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
