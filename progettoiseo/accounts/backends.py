from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Autenticazione personalizzata che permette login con email o username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
            
        try:
            # Cerca l'utente per username o email
            user = User.objects.get(
                Q(username=username) | Q(email=username)
            )
        except User.DoesNotExist:
            # Esegui check password anche se l'utente non esiste
            # per evitare timing attacks
            User().check_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Se ci sono più utenti con la stessa email, usa il primo
            user = User.objects.filter(
                Q(username=username) | Q(email=username)
            ).first()
            
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None