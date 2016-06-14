from __future__ import unicode_literals

from django.db import models

from gestione_utenti.models import Utente

from gestione_catalogo.models import OggAsta

from django.utils import timezone
# Create your models here.

class Puntata(models.Model):
    importo = models.IntegerField(default=0.01)
    data = models.DateTimeField()
    idasta = models.ForeignKey(OggAsta, default=None)
    vincente = models.ForeignKey(Utente)

    def __unicode__(self):
        return str(self.id)
