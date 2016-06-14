from django.contrib import admin
from .models import OggAsta, Utente, Categoria
# Register your models here.

class OggAstaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nome']}),
        (None, {'fields': ['descrizione']}),
        ('Date information', {'fields': ['data']}),
        ('Date information', {'fields': ['scadenza']}),
        ('Utente', {'fields': ['creatoda']}),
        ('Categoria', {'fields': ['tipo']}),
        # opzione collapse
    ]
    list_display = ('nome', 'aste_valide')

    # Filtri sui dati
    list_filter = ['scadenza']

    # Funzioni di ricerca
    search_fields = ['nome']
    date_hierarchy = 'data'


admin.site.register(OggAsta, OggAstaAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nome']}),
        (None, {'fields': ['descrizione']}),
        # opzione collapse
        # ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]


admin.site.register(Categoria, CategoriaAdmin)