from django.contrib import admin
from .models import  Utente
# Register your models here.

class UtenteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
        (None, {'fields': ['password']}),
        (None, {'fields': ['nome']}),
        (None, {'fields': ['cognome']}),
        (None, {'fields': ['indirizzo']}),
        (None, {'fields': ['email']}),
        # opzione collapse
        # ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]


admin.site.register(Utente, UtenteAdmin)