# coding=utf-8
# -*- coding: utf-8 -*
# from forms import ContactForm, StatoForm

# -*- coding: utf-8 -*
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from models import *
from gestione_acquisti.models import Puntata


# Create your views here.

def scadenze(request):
    ''''parte che viene visualizzata nell'homepage'''
    # ogg=models.OggAsta.aste_valide()
    # sorted(ogg)

    #    '''visualizza le ultime 10 aste in scadenza'''

    template_name = 'AsteOnLine/index.html'
    context_object_name = 'aste_recenti'
    latest_aste_list = [a for a in OggAsta.objects.order_by('scadenza') if a.aste_valide()][:10]
    #puntate_list = [a for a in Puntata.objects.all() if OggAsta.objects.filter(id=a.idasta) in latest_aste_list]
    puntate_list = Puntata.objects.all()
    quan=0
    for i in latest_aste_list:
        quan+=1

    print "quant=",
    print quan
    l=[]
    for i in xrange(0,quan) :
        print "---"
        print latest_aste_list[i].nome
        for j in puntate_list:
            print "almeno una puntata c'è?"
            print j.idasta
            if j.idasta==latest_aste_list[i]:
                l.append(j)
                print "almeno una volta dovresti entrare"
                print j.importo
                break
    # puntate_aste = Puntata.objects.filter(latest_aste_list=OggAsta).last()
    # l=[]
    # puntate_aste=[]
    # print "ciao"
    # for i in latest_aste_list:
    #   l.append(i)
    #   print i.id
    #   print i.nome
    #  #puntate_aste.append(Puntata.objects.select_related(i.nome))
    #  puntate_aste.append(Puntata.objects.filter(i=OggAsta).last())
    # guarda conversazione e consigli di torre
    context = {'aste': latest_aste_list, 'puntate':l, 'numeri':xrange(1,quan)}  # , 'puntate': puntate_aste}
    # output = ', '.join([p.nome for p in latest_aste_list])
    return render(request, 'gestione_catalogo/index.html', context)

    # return context


# template_name = 'gestione_catalogo/index.html'
# return HttpResponse(request)
# return render(request, 'gestione_catalogo/index.html', {'messaggio': 'ciao'})
'''
riporta tutte le categorie
'''


@login_required(login_url='/portale/login')
def riporta_categorie(request):
   all_categorie_list = Categoria.objects.all()
   context = {'categorie': all_categorie_list}
   return render(request, 'gestione_catalogo/categorie.html', context)

#@login_required(login_url='/portale/login')
#class Categorie(generic.ListView):
#    """
#    Classe che tramite i generics di Django implementa la visualizzazione per categorie del sito
#    """
#    template_name = 'gestione_catalogo/categorie.html'
#    context_object_name = 'categorie'

#    def get_queryset(self):
#        """
#        Ricava la lista delle categorie
#        :return: la lista
#        """
#        return Categoria.objects.all()


'''
riporta le prime 4 aste in scadenza e scadute per la categoria selezionata
'''

@login_required(login_url='/portale/login')
def riporta_astecategorie(request, idcategoria):
    '''
    get_object_or_404 funzione unica per gestire l'errore eventuale
    '''
    categoria = get_object_or_404(Categoria, pk=idcategoria)

    list_aste_categorie_in_scadenza = [a for a in OggAsta.objects.filter(tipo=idcategoria).order_by('scadenza') if
                                       a.aste_valide()]
    list_aste_categorie_scadute = [a for a in OggAsta.objects.filter(tipo=idcategoria).order_by('scadenza') if
                                   not a.aste_valide()]

    list_puntate_in_scadenza= Puntata.objects.all()
    #così ho tutte le punbtate
    #mi interessano però solo le puntate più alte per ogni oggetto
    l=[]
    for i in list_aste_categorie_in_scadenza:
        list_perogg = []
        for j in list_puntate_in_scadenza:
            #recupero tutte le aste per tale oggetto

            if(j.idasta==i):
                list_perogg.append(j)
        #ho tutte le aste per questo oggetto, devo recuperare loa più alta (l'ultima)
        punt=0
        for j in list_perogg:
            if punt==0:
                punt=j
            if punt.importo <= j.importo:
                punt=j
        l.append(punt)

    list_puntate_in_scadenza=l
    print "stampa aste in scadenza"
    for i in list_puntate_in_scadenza:
        print i

    list_puntate_scadute = Puntata.objects.all()
    # così ho tutte le punbtate
    # mi interessano però solo le puntate più alte per ogni oggetto
    l = []
    for i in list_aste_categorie_scadute:
        list_perogg = []
        for j in list_puntate_scadute:
            # recupero tutte le aste per tale oggetto

            if (j.idasta == i):
                list_perogg.append(j)
        # ho tutte le aste per questo oggetto, devo recuperare loa più alta (l'ultima)
        punt = 0
        #print "ci sono"
        #print len(list_perogg)
        for j in list_perogg:
            #print "entro*"
            if punt == 0:
                punt = j
            if punt.importo <= j.importo:
                punt = j
        l.append(punt)

    list_puntate_scadute = l
    print "stampa aste scadute"
    for i in list_puntate_scadute:
        print i
        #print i.importo

    context = {'in_scadenza': list_aste_categorie_in_scadenza, 'scadute': list_aste_categorie_scadute,
               'categoria': categoria, 'puntatein':list_puntate_in_scadenza, 'puntatesca':list_puntate_scadute}
    return render(request, 'gestione_catalogo/astecategoria.html', context)


@login_required(login_url='/portale/login')
def astacreata(request):
    list_aste_inscadenza = [a for a in OggAsta.objects.filter(creatoda=request.user).order_by('scadenza') if
                                       a.aste_valide()]
    list_aste_scadute = [a for a in OggAsta.objects.filter(creatoda=request.user).order_by('scadenza') if not
                                       a.aste_valide()]
    titolo1="Aste in scadenza"
    titolo2="Aste scadute"

    list_puntate_in_scadenza = Puntata.objects.all()
    # così ho tutte le punbtate
    # mi interessano però solo le puntate più alte per ogni oggetto
    l = []
    for i in list_aste_inscadenza:
        list_perogg = []
        for j in list_puntate_in_scadenza:
            # recupero tutte le aste per tale oggetto

            if (j.idasta == i):
                list_perogg.append(j)
        # ho tutte le aste per questo oggetto, devo recuperare loa più alta (l'ultima)
        punt = 0
        for j in list_perogg:
            if punt == 0:
                punt = j
            if punt.importo <= j.importo:
                punt = j
        l.append(punt)
    list_puntate_in_scadenza = l
    list_puntate_scadute = Puntata.objects.all()
    # così ho tutte le punbtate
    # mi interessano però solo le puntate più alte per ogni oggetto
    l = []
    for i in list_aste_scadute:
        list_perogg = []
        for j in list_puntate_scadute:
            # recupero tutte le aste per tale oggetto

            if (j.idasta == i):
                list_perogg.append(j)
        # ho tutte le aste per questo oggetto, devo recuperare loa più alta (l'ultima)
        punt = 0
        # print "ci sono"
        # print len(list_perogg)
        for j in list_perogg:
            # print "entro*"
            if punt == 0:
                punt = j
            if punt.importo <= j.importo:
                punt = j
        l.append(punt)

    list_puntate_scadute = l

    titolo="Le mie aste create"
    oggetto = {"titolo":titolo, "titolo1": titolo1, "titolo2": titolo2, "inscadenza": list_aste_inscadenza,
               "scadute": list_aste_scadute, 'puntatein':list_puntate_in_scadenza, 'puntatesca':list_puntate_scadute}


    return render(request, "gestione_catalogo/lemieaste.html", oggetto)

@login_required(login_url='/portale/login')
def astapart(request):
    #aste a cui ho partecipato, scadute e in scadenza.

    #passi:
    #recupero tutte le puntate (non dell'utente perchè altrimenti dopo non riesco a sapere se è la prima puntata  o meno
    #per ogni oggetto esistente, trovo tutte le sue puntate
    #se per tale oggetto ce n'è una allora nessuno ha partecipato a tale asta (è stata solo creata)
    #se per tale oggetto la prima puntata è dell'utente allora non ha partecipato alla sua stessa asta perchè non può
    #se invece poi c'è l'utente tra i vincenti, allora aggiungi tale asta o alla lista delle scadute o alla lista di quelle in scadenza


    list_tutte_punt = Puntata.objects.all()
    #recupero gli oggetti per cui ha puntato
    oggaste_insca = []
    oggaste_sca =[]
    list_tutti_ogg = OggAsta.objects.all()

    for i in list_tutti_ogg:
        list_puntate_ogg = []
        list_puntate_ogg = Puntata.objects.filter(idasta=i).order_by("data")
        #nessuno ha partecipato all'asta
        if len(list_puntate_ogg)<=1:
            continue
        #l'hai creata tu
        if list_puntate_ogg[0].vincente == request.user:
            continue
        vincenti = [v.vincente for v in list_puntate_ogg]
        if request.user in vincenti:
            if i.aste_valide():
                oggaste_insca.append(i)
            else:
                oggaste_sca.append(i)

    #devo recuperare le puntate delle aste non ancora scadute
    list_puntate_in_scadenza = Puntata.objects.all()
    # così ho tutte le punbtate
    # mi interessano però solo le puntate più alte per ogni oggetto
    l = []
    for i in oggaste_insca:
        list_perogg = []
        for j in list_puntate_in_scadenza:
            # recupero tutte le aste per tale oggetto

            if (j.idasta == i):
                list_perogg.append(j)
        # ho tutte le aste per questo oggetto, devo recuperare loa più alta (l'ultima)
        punt = 0
        for j in list_perogg:
            if punt == 0:
                punt = j
            if punt.importo <= j.importo:
                punt = j
        l.append(punt)
    list_puntate_in_scadenza = l

    titolo1 = "Aste in scadenza"
    titolo2 = "Aste scadute"
    titolo="Aste a cui ho partecipato"
    oggetto = {"titolo":titolo, "titolo1": titolo1, "titolo2": titolo2, "inscadenza": oggaste_insca,
               "scadute": oggaste_sca, 'puntatein': list_puntate_in_scadenza}

#OCCHIO DEVO TOGLIERE LE ASTE CHE HO CREATO IO!! OVVERO QUELLE PUNTATE PRIME CHE HO FATTO

    return render(request, "gestione_catalogo/lemieaste.html", oggetto)


@login_required(login_url='/portale/login')
def astavinta(request):

    titolo1=""
    titolo2="Aste vinte"
    #devo recuperare tutte le puntate, separarle per ogg.asta, prendere la puntata con importo più grande e verificare che sia l'utente
    #OCCHIO: se però è l'unica puntata per tale oggetto allora lo ha creato l'utente e quindi non lo ha vinto

    list_puntate = Puntata.objects.all()
    lista_ogg = OggAsta.objects.all()
    lista_vittorie = []
    lista_vit_pun = []
    for i in lista_ogg:
        #setto la lista di tutte le sue puntate a vuota
        l=[]
        for j in list_puntate:
            if j.idasta == i:
                l.append(j)

        #se la lista ha un solo oggetto, allora vuol dire che non ci sono puntate,
        #l'unica puntata è di chi ha creati l'oggetto
        if len(l)==1:
            continue

        #anche se l'oggetto non è ancora scaduto allora saltalo: non è stato vinto
        if i.aste_valide():
            continue

        l=l[1:]
        max=-1
        for j in l:
            if max==-1:
                max=j
            if max.importo < j.importo:
                max=j
        if max==-1:
            continue
        if max.vincente == request.user:
            lista_vittorie.append(i)
            lista_vit_pun.append(max)
    titolo = "Aste vinte"
    oggetto = {"titolo":titolo, "titolo1": titolo1, "titolo2": titolo2,
               "scadute": lista_vittorie, 'puntatesca':lista_vit_pun}

    list_puntate_in_scadenza = l
    return render(request, "gestione_catalogo/lemieaste.html", oggetto)

