from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from gestione_utenti.models import Utente


# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome

    def trova_categoria(self, scelta):
        return self.nome == scelta


class OggAsta(models.Model):
    nome = models.CharField(max_length=30)
    data = models.DateTimeField()
    scadenza = models.DateTimeField()
    descrizione = models.CharField(max_length=50)
    creatoda = models.ForeignKey(Utente)
    tipo = models.ForeignKey(Categoria)

    def __unicode__(self):
        return self.nome

    def aste_valide(self):
        return self.scadenza > timezone.now()

        # aste_valide.admin_order_field = 'scadenza'
        # aste_valide.boolean = True
        # aste_valide.short_description = 'Published ?'
