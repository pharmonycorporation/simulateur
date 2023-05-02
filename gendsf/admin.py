from django.contrib import admin

from .models import *
from django.template.response import TemplateResponse
from django.urls import path



admin.site.register(Identification)
admin.site.register(Pays)
admin.site.register(Service)
admin.site.register(DSF)
admin.site.register(DADS)
admin.site.register(FormeJuridique)
admin.site.register(ControleEntreprise)
admin.site.register(RegimeFiscale)
admin.site.register(FicheFiscale)
admin.site.register(Dirigeants)
admin.site.register(MembreConseil)
admin.site.register(FicheEffectif)
admin.site.register(FicheVerSementTVA)
admin.site.register(FicheVersementAccompteIS)
admin.site.register(BalanceSixColonneSYSCohada)
admin.site.register(InformationsAutres)
admin.site.register(FicheVersementSpontaneIRPP)
admin.site.register(EtatSalaire)
admin.site.register(ServiceConseil)


