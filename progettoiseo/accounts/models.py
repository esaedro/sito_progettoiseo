from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

# Create your models here.

class ProfiloUtente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    numero_tessera = models.CharField(max_length=20, unique=True, blank=True, null=True)
    immagine_profilo = models.ImageField(upload_to='immagini_di_profilo/', blank=True, null=True)
    data_tesseramento = models.DateField(blank=True, null=True)

    objects = models.Manager()

    @classmethod
    def get_profilo_utente(cls, user) -> 'ProfiloUtente':
        return cls.objects.get(user=user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from datetime import datetime
        from django.contrib.auth.models import Group
        
        # Crea il profilo con dati iniziali
        profilo = ProfiloUtente.objects.create(user=instance)
        
        # Inizializza i dati del profilo
        if '@' in instance.username:
            # Se username è un'email, impostala anche come email dell'utente
            instance.email = instance.username
            instance.save()
        
        # Imposta data tesseramento e numero tessera
        profilo.data_tesseramento = datetime.now()
        profilo.numero_tessera = profilo.data_tesseramento.strftime('%Y%m%d%H%M%S')
        profilo.save()
        
        # Assegna automaticamente l'utente al gruppo "Tesserato"
        try:
            gruppo_tesserato, created_group = Group.objects.get_or_create(name='Tesserato')
            instance.groups.add(gruppo_tesserato)
        except Exception as e:
            # Log dell'errore se necessario, ma non bloccare la creazione dell'utente
            print(f"Errore nell'assegnazione del gruppo: {e}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profiloutente'):
        instance.profiloutente.save()
