from django.contrib import admin
from .models import TarifDouanier,TVA, Pays,ModePaiement,MoyenTransport,Devise, Simulation, RegimeFiscale
# Register your models here.
admin.site.register(TarifDouanier)
admin.site.register(TVA)
admin.site.register(Pays)
admin.site.register(ModePaiement)
admin.site.register(MoyenTransport)
admin.site.register(Devise)
admin.site.register(Simulation)
admin.site.register(RegimeFiscale)
