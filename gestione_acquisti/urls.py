from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<id_asta>[0-9]+)$', views.riporta_dettagli, name='elem_asta'),
]