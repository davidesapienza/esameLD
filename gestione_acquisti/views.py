# coding=utf-8
from django.shortcuts import render
from gestione_utenti.models import Utente
from gestione_catalogo.models import OggAsta, Categoria
from models import Puntata
from django.utils import timezone
from django.db import IntegrityError


# Create your views here.

def riporta_dettagli(request, id_asta):
    elemento = OggAsta.objects.filter(id=id_asta)
    puntata = Puntata.objects.filter(idasta=id_asta)
    scadenza = False
    elemento = elemento[0]
    if elemento.aste_valide():
        scadenza = True
    puntata = puntata.last()
    if request.method == "POST":
        # se l'utente è lo stesso di chi ha creato l'asta allora non può puntare
        utentecreatore = Puntata.objects.filter(idasta=id_asta)
        # recupero la prima puntata che appartiene a colui che l'ha creata
        utentecreatore = utentecreatore[0]
        utentecreatore = utentecreatore.vincente
        if utentecreatore == request.user:
            messaggio = "non puoi partecipare alla tua stessa asta"
            return render(request, 'gestione_acquisti/dettagli.html',
                          {'messaggio': messaggio, 'asta': elemento, 'puntata': puntata, 'scadenza': scadenza})
        # se l'utente è lo stesso di chi sta vincendo l'asta non può votare
        utenteultimo = Puntata.objects.filter(idasta=id_asta).last()
        utenteultimo = utenteultimo.vincente
        if utenteultimo == request.user:
            messaggio = "Attenzione! la puntata più alta è già la tua"
            return render(request, 'gestione_acquisti/dettagli.html',
                          {'messaggio': messaggio, 'asta': elemento, 'puntata': puntata, 'scadenza': scadenza})

        #se non punto niente devo rimostrare la pagina e basta
        if request.POST['puntata']=="":
            messaggio = ""
            return render(request, 'gestione_acquisti/dettagli.html',
                          {'messaggio': messaggio, 'asta': elemento, 'puntata': puntata, 'scadenza': scadenza})

        # se la puntata attuale è minore o uguale alla puntata ultima, allora non va bene errore
        puntataultima = Puntata.objects.last()
        print "puntataultima:",
        print puntataultima.importo
        print "puntata:",
        print request.POST['puntata']
        a=request.POST['puntata']
        print a
        b=puntataultima.importo
        print b
        if int(a) <= int(b):
            print "entri qui?"
            messaggio = "non puoi puntare meno del valore attuale dell'asta"
            return render(request, 'gestione_acquisti/dettagli.html',
                          {'messaggio': messaggio, 'asta': elemento, 'puntata': puntata, 'scadenza': scadenza})

        # se arrivo qui l'ultimo inconveniente potrebbe essere che nel frattempo l'asta è scaduta
        if scadenza == False:
            messaggio = "siamo spiacenti! l'asta è scaduta"
            return render(request, 'gestione_acquisti/dettagli.html',
                          {'messaggio': messaggio, 'asta': elemento, 'puntata': puntata, 'scadenza': scadenza})

        # qui invece posso aggiungere la puntata
        try:
            print "ma qui arrivi?"
            puntatavera = Puntata.objects.create(idasta=OggAsta.objects.filter(id=id_asta).get(), vincente=request.user, importo=request.POST["puntata"],data=timezone.now())
            puntatavera.save()
            puntata = Puntata.objects.filter(idasta=id_asta).last()
        except IntegrityError:
            messaggio = "errore in creazione puntata"
            return render(request, 'gestione_acquisti/dettagli.html',
                          {'messaggio': messaggio, 'asta': elemento, 'puntata': puntata, 'scadenza': scadenza})
    messaggio=""
    return render(request, 'gestione_acquisti/dettagli.html',
                  {'messaggio': messaggio, 'asta': elemento, 'puntata': puntata, 'scadenza': scadenza})
