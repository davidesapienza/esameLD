from django import forms
from django.forms import ModelForm
from gestione_catalogo.models import *

'''
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
'''

'''
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter']
'''


class NuovaAsta(ModelForm):
    scadenza = forms.DateTimeField( initial=timezone.now())
    class Meta:
        model = OggAsta
        fields = ['nome', 'scadenza', 'descrizione', 'tipo']
        labels = ['Nome Oggetto', 'Data Scadenza', 'Descrizione', 'Categoria']
