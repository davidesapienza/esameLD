from django.contrib import admin
from .models import Puntata


# Register your models here.

class PuntataAdmin(admin.ModelAdmin):
    fieldsets = [
         ('Utente', {'fields': ['vincente']}),
         ('Oggetto', {'fields': ['idasta']}),
         (None, {'fields': ['importo']}),
         ('Date information', {'fields': ['data']}),
        # opzione collapse
        #    ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]


admin.site.register(Puntata, PuntataAdmin)
