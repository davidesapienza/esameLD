from django.conf.urls import url
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r'^$', views.scadenze, name='index'),
    url(r'^$', views.portal_main_page, name='profilo'),
    url(r'^login$', views.mylogin, name='login'),
    url(r'^logout$', views.mylogout, name='logout'),
    url(r'^registrazione$', views.registrazione, name='registrazione'),
    url(r'^crea_asta$', login_required(views.crea_asta, login_url='/portale/login'), name='crea_asta'),

    url(r'^about-us$', login_required(views.contattaci, login_url='/portale/login'), name='contattaci'),
]