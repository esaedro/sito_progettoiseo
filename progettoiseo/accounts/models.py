from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

# Create your models here.

class ProfiloUtente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    numero_tessera = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    immagine_profilo = models.ImageField(upload_to='immagini_di_profilo/', blank=True, null=True)
    data_tesseramento = models.DateField(blank=True, null=True)

    objects = models.Manager()

    @classmethod
    def get_profilo_utente(cls, user) -> 'ProfiloUtente':
        return cls.objects.get(user=user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfiloUtente.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profiloutente'):
        instance.profiloutente.save()
