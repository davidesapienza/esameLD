from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.scadenze, name='index'),
    url(r'^categorie$', login_required(views.riporta_categorie, login_url='/portale/login'), name='categorie'),
    #url(r'^categorie$', login_required(views.Categorie.as_view(), login_url='/portale/login'), name='categorie'),

    url(r'^categorie/(?P<idcategoria>[0-9]+)$', login_required(views.riporta_astecategorie, login_url='/portale/login'), name='aste_categorie'),
    url(r'^aste_create$', login_required(views.astacreata, login_url='/portale/login'), name='asta_creata'),
    url(r'^aste_partecipate$', login_required(views.astapart, login_url='/portale/login'), name='asta_partecipata'),
    url(r'^aste_vinte$', login_required(views.astavinta, login_url='/portale/login'), name='asta_vinta'),
    ]
