# -*- coding: utf-8 -*
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from gestione_utenti.models import Utente
from django.core.mail import send_mail
from gestione_utenti.forms import NuovaAsta
from models import *
from gestione_acquisti.models import *
from django.utils import timezone
def mylogin(request):  # , next):

    '''
parte copiata dalle slide
    username =
    request.POST['username']
    password =
    request.POST['password']
    user =
    authenticate
    (username = username, password = password)
    if user is not None:
        if user.is_active:
            login
    (request, user)
    # Redirect to a success page.
    else:
    # Return a 'disabled account' error message
    else:
    # Return an 'invalid login' error message
    '''
    if request.method == 'POST':
        print "sei entrato con post?"

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        next_url=request.POST.get("next",None)
        if user is not None:
            print "user diverso da none"
            if user.is_active:
                print "user attivo"
                login(request, user)
                # Redirect to a success page.
                # if next != "":
                #    return HttpResponseRedirect(next)
                # else:
                print next_url
                if next_url == 'None':
                    print "next_url none"
                    next_url=reverse('gestione_catalogo:index')
                print next_url
                return HttpResponseRedirect(next_url)


            else:
                # Return a 'disabled account' error message
                render(request, 'gestione_utenti/login.html', {'messaggio': 'disabled account', 'next_url':next_url})
        else:
            # Return an 'invalid login' error message
            return render(request, 'gestione_utenti/login.html', {'messaggio': 'Nome utente o password errati!', 'next_url':next_url})
    else:
        if request.user.is_anonymous():
            # entra in questo caso quando voglio fare il login (devo ancora inserire user e pwd
            print "anonimo"
            return render(request, 'gestione_utenti/login.html', {'next_url':request.GET.get('next',None)})
        else:
            print "questo è il caso"
            return HttpResponseRedirect(reverse('gestione_catalogo:index'))
            # return HttpResponseRedirect('/')


#def registrazione(request):
#    return render(request, 'gestione_utenti/registrazione.html', {'messaggio': 'registrazione'})


def registrazione(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        passwordconf = request.POST['passwordconf']
        nome = request.POST['nome']
        cognome = request.POST['cognome']
        email = request.POST['email']
        indirizzo = request.POST['indirizzo']
        if (passwordconf == '' or password != passwordconf):
            return render(request, 'gestione_utenti/registrazione.html', {'messaggio': 'pwd e pwd di conferma errate'})

        if (username == '' or nome == '' or cognome == '' or email == '' or indirizzo == ''):
            utente_fields = {'username': username, 'nome': nome, 'cognome': cognome, 'email': email,
                             'indirizzo': indirizzo, 'messaggio': 'compila tutti i campi obbligatori'}
            return render(request, 'gestione_utenti/registrazione.html', utente_fields)
        try:
            user = Utente.objects.create_user(username=username, email=email, password=password,
                                              nome=nome, cognome=cognome, indirizzo=indirizzo)
            user.is_active = True
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            # key=user.username+stringa_random()

            # att = key_tab.objects.create(utente=user,key=key)
            # subject = 'Attivazione account'
            # link = reverse('gestione_utenti:attivazione',kwargs={'key':key})
            # message = 'Attiva il tuo account visitando:\n'+'http://127.0.0.1:8000'+link
            # sender = 'noreply.asteonline@gmail.com'
            # recipients=[email]
            # send_mail(subject, message, sender, recipients)
            # info={'titolo':'Utente registrato correttamente','corpo':'Verifica la mail per attivare il tuo account'}
            return render(request, 'gestione_utenti/profile.html', {
                'messaggio': 'Registrazione effettuata con successo, ora puoi navigare liberamente per il sito'})
        except IntegrityError:
            utente_fields = {'nome': nome, 'cognome': cognome, 'email': email, 'indirizzo': indirizzo,
                             'messaggio': 'Username non valido'}
            return render(request, 'gestione_utenti/registrazione.html', utente_fields)
    else:
        if request.user.is_anonymous():
            return render(request, 'gestione_utenti/registrazione.html')
        else:
            return HttpResponseRedirect(reverse('gestione_utenti:profile'))


@login_required(login_url='/portale/login')
def portal_main_page(request):
    """
    Gestisce la pagina personale.
    :param request: la richiesta
    :return: il render del template
    """
    messaggio = "Grazie per aver effettuato il login, ora puoi navigare liberamente per il sito"
    return render_to_response('gestione_utenti/profile.html', {'request': request, 'messaggio': messaggio})


def mylogout(request):
    """
    Permette all'utente che effettua la richiesta di uscire dalla sessione
    :param request: la richiesta
    :return: il render alla pagina di login
    """
    logout(request)
    return HttpResponseRedirect(reverse('gestione_utenti:login'))
@login_required(login_url='/portale/login')
def crea_asta(request):
    if request.method == "POST":
        form = NuovaAsta(request.POST)
        if form.is_valid():
            print "non sarai mica valida"
            try:
                ogg = form.save(commit=False)
                ogg.data = timezone.now()
                if ogg.scadenza <= ogg.data:
                    return render(request,
                                  'gestione_utenti/creaasta.html', {'form': form, 'messaggio': 'scadenza errata!'})
                if request.POST['importo'] <= 0.01:
                    return render(request,
                                  'gestione_utenti/creaasta.html', {'form': form, 'messaggio': "base d'asta errata!"})
                ogg.creatoda = Utente.objects.filter(id=request.user.id).last()
                print Utente.objects.filter(id=request.user.id).last()
                ogg.save()
                print ogg.id
                ##
                puntata = Puntata.objects.create(importo=request.POST['importo'], data=timezone.now(), idasta=ogg,
                                                      vincente=ogg.creatoda)
                #user.is_active = True
                puntata.save()
                url = reverse('gestione_acquisti:elem_asta', kwargs={'id_asta':ogg.id})
                return HttpResponseRedirect(url)
                #return HttpResponseRedirect(reverse('gestione_acquisti:elem_asta', args=(ogg.id,), kwargs={'id_asta':ogg.id}))
                #return HttpResponseRedirect(reverse('gestione_acquisti:elem_asta', kwargs={'id_asta': ogg.id}))
            except IntegrityError:
                return render(request, 'gestione_utenti/creaasta.html', {'form':form})

        else:
            messaggio="Errore in inserimento campi"
            return render(request, 'gestione_utenti/creaasta.html', {'messaggio':messaggio, 'form':form})
    else:
        form = NuovaAsta()
        #form.scadenza = timezone.now()
        form.scadenza = timezone.now()
        print timezone.now()
        print form.scadenza
        return render(request, 'gestione_utenti/creaasta.html', {'form':form})
@login_required(login_url='/portale/login')
def contattaci(request):
    if request.method == 'POST':
        name=request.POST['Name']
        mail=request.POST['contact-email']
        mess=request.POST['contact-message']
        print "ci siamo"
        if name=='' or mail=='':
            print "nome-mail"
            oggetto = {"utente": request.user, "messaggio": "Nome-Cognome e indirizzo email sono obbligatori"}
            return render(request, "gestione_utenti/contact-us.html", oggetto)
        if mess=='':
            print "messaggio"
            oggetto = {"utente": request.user, "messaggio": "Attenzione: non ha scritto nessun messaggio"}
            return render(request, "gestione_utenti/contact-us.html", oggetto)
        #altrimenti devo mandare una mail.
        oggmess = "messaggio-sitoaste di "+name
        recipients = ['noreply.asteonline@gmail.com']
        send_mail(oggmess, mess, mail, recipients)
        oggetto = {"utente": request.user, "messaggio": "Messaggio inviato"}
        return render(request, "gestione_utenti/contact-us.html", oggetto)


    else:
        oggetto={"utente":request.user, "messaggio":""}
        return render(request, "gestione_utenti/contact-us.html", oggetto)