from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
class Utente(AbstractUser):
    nome = models.CharField(max_length=20)
    cognome = models.CharField(max_length=30)
    indirizzo = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome
