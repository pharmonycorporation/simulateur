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
from simulateur import views as simviews
from gestionlicence import views as web_views
router = routers.DefaultRouter()
router.register(r'dsfs', views.DSFViewSet)
router.register(r'dads', views.DADSViewSet)
router.register(r'dsffile', views.DSFFileViewSet)
router.register(r'filedads', views.DADSFileViewSet)
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
    # path('',include('gestionlicence.urls')),
    path('',simviews.SignInView.as_view(),name='authentication'),
     path('signin/', web_views.SignInView.as_view(), name="signin"),
    path('signup/', web_views.SignupView.as_view(), name="signup"),
    path('logout/', web_views.signout, name="signout"),
    path('profile/', web_views.ProfileView.as_view(), name="profile"),
    path('sim', simviews.initialisationTarif),
    path('mon', simviews.initialisationMonaie),
    path('authentication', simviews.SignInView.as_view(),name='authentication'),
    path('registration', simviews.SignupView.as_view(),name='registration'),
    path('pays', simviews.initialisationPays),
    path('test', simviews.ajuster),
    path('sup', simviews.suppression),
    path('init_regime_douanier', simviews.regimeDouanier),
    path('init_mode_paiement', simviews.modePaiement),
    path('init_moyen_transport', simviews.moyenTransport),
    path('sdi', simviews.home, name='sdi'),
    path('tarification', simviews.index, name='tarification'),
    path('tec', simviews.tecView, name='tec'),
    path('up_profile', simviews.ProfileView.as_view(), name='up_profile'),
    path('mes_simulations', simviews.SimulationView.as_view(), name='mes_simulations'),
    path('ajax_gettarif/', simviews.getProd, name='ajax_gettarif'),
    path('gettarifs/', simviews.getProduits, name='gettarifs'),
    path('demarrerSimulateur/', simviews.demarrerSimulateur, name='demarrerSimulateur'),
    path('dsf_api/', include(router.urls)),
    path('paypal/', include('paypal.standard.ipn.urls')),
]

handler404 = "gestionlicence.views.page_not_found"
handler500 = "gestionlicence.views.server_error"
