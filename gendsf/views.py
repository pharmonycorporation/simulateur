from django.shortcuts import render
from .serializers import ServiceConseilSerializer, DSFSerializer, DADSSerializer,  PaysSerializer, FormeJuridiqueSerializer,EtatSalaireSerializer, ServiceSerializer, InformationsAutresSerializer,FicheVersementSpontaneIRPPSerializer, BalanceSixColonneSYSCohadaSerializer, FicheVersementAccompteISSerializer, FicheVerSementTVASerializer,DirigeantsSerializer,FicheEffectifSerializer,MembreConseilSerializer, FicheFiscaleSerializer,ControleEntrepriseSerializer, IdentificationSerializer, RegimeFiscaleSerializer
from .models import DSF, DADS, ServiceConseil, Pays, FormeJuridique,EtatSalaire, Service, InformationsAutres,FicheVersementSpontaneIRPP, BalanceSixColonneSYSCohada, FicheVersementAccompteIS, FicheVerSementTVA,Dirigeants,FicheEffectif,MembreConseil, FicheFiscale,ControleEntreprise, Identification, RegimeFiscale
from rest_framework import routers, serializers, viewsets
# Create your views here.

class DSFViewSet(viewsets.ModelViewSet):
    queryset = DSF.objects.all()
    serializer_class = DSFSerializer

class DADSViewSet(viewsets.ModelViewSet):
    queryset = DADS.objects.all()
    serializer_class = DADSSerializer

class ServiceConseilViewSet(viewsets.ModelViewSet):
    queryset = ServiceConseil.objects.all()
    serializer_class = ServiceConseilSerializer

class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer

class FormeJuridiqueViewSet(viewsets.ModelViewSet):
    queryset = FormeJuridique.objects.all()
    serializer_class = FormeJuridiqueSerializer

class EtatSalaireViewSet(viewsets.ModelViewSet):
    queryset = EtatSalaire.objects.all()
    serializer_class = EtatSalaireSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class InformationsAutresViewSet(viewsets.ModelViewSet):
    queryset = InformationsAutres.objects.all()
    serializer_class = InformationsAutresSerializer

class FicheVersementSpontaneIRPPViewSet(viewsets.ModelViewSet):
    queryset = FicheVersementSpontaneIRPP.objects.all()
    serializer_class = FicheVersementSpontaneIRPPSerializer

class BalanceSixColonneSYSCohadaViewSet(viewsets.ModelViewSet):
    queryset = BalanceSixColonneSYSCohada.objects.all()
    serializer_class = BalanceSixColonneSYSCohadaSerializer

class FicheVersementAccompteISViewSet(viewsets.ModelViewSet):
    queryset = FicheVersementAccompteIS.objects.all()
    serializer_class = FicheVersementAccompteISSerializer

class FicheVerSementTVAViewSet(viewsets.ModelViewSet):
    queryset = FicheVerSementTVA.objects.all()
    serializer_class = FicheVerSementTVASerializer

class DirigeantsViewSet(viewsets.ModelViewSet):
    queryset = Dirigeants.objects.all()
    serializer_class = DirigeantsSerializer

class FicheEffectifViewSet(viewsets.ModelViewSet):
    queryset = FicheEffectif.objects.all()
    serializer_class = FicheEffectifSerializer

class MembreConseilViewSet(viewsets.ModelViewSet):
    queryset = MembreConseil.objects.all()
    serializer_class = MembreConseilSerializer

class FicheFiscaleViewSet(viewsets.ModelViewSet):
    queryset = FicheFiscale.objects.all()
    serializer_class = FicheFiscaleSerializer

class ControleEntrepriseViewSet(viewsets.ModelViewSet):
    queryset = ControleEntreprise.objects.all()
    serializer_class = ControleEntrepriseSerializer

class IdentificationViewSet(viewsets.ModelViewSet):
    queryset = Identification.objects.all()
    serializer_class = IdentificationSerializer

class RegimeFiscaleViewSet(viewsets.ModelViewSet):
    queryset = RegimeFiscale.objects.all()
    serializer_class = RegimeFiscaleSerializer