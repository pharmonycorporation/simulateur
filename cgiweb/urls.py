"""cgiweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from gendsf import views
from rest_framework import routers, serializers, viewsets
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'dsfs', views.DSFViewSet)
router.register(r'dads', views.DADSViewSet)
router.register(r'services', views.ServiceConseilViewSet)
router.register(r'listeservices', views.ServiceViewSet)
router.register(r'pays', views.PaysViewSet)
router.register(r'formejuridique', views.FormeJuridiqueViewSet)
router.register(r'regimefiscale', views.RegimeFiscaleViewSet)
router.register(r'etatsalaire', views.EtatSalaireViewSet)
router.register(r'informationsautres', views.InformationsAutresViewSet)
router.register(r'ficheirppv', views.FicheVersementSpontaneIRPPViewSet)
router.register(r'balancesixcolonne', views.BalanceSixColonneSYSCohadaViewSet)
router.register(r'ficheversementis', views.FicheVersementAccompteISViewSet)
router.register(r'ficheversementva', views.FicheVerSementTVAViewSet)
router.register(r'dirigeants', views.DirigeantsViewSet)
router.register(r'ficheeffectif', views.FicheEffectifViewSet)
router.register(r'membreconseil', views.MembreConseilViewSet)
router.register(r'controleentreprise', views.ControleEntrepriseViewSet)
router.register(r'identification', views.IdentificationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('gestionlicence.urls')),
    path('dsf_api/', include(router.urls)),
    path('paypal/', include('paypal.standard.ipn.urls')),
]

handler404 = "gestionlicence.views.page_not_found"
handler500 = "gestionlicence.views.server_error"
