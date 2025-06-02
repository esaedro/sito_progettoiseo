from django.db import models

# Create your models here.

class Utente(models.Model):
    numero_tessera = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    immagine_profilo = models.ImageField(upload_to='immagini_di_profilo/', blank=True, null=True)
    data_tesseramento = models.DateField()


    def __str__(self):
        return f"{self.email}"

    class Meta:
        db_table = 'utenti'
