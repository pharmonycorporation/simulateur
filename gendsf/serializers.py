from django.urls import path, include
from .models import DSF, DADS, ServiceConseil, Pays, FormeJuridique,EtatSalaire, Service, InformationsAutres,FicheVersementSpontaneIRPP, BalanceSixColonneSYSCohada, FicheVersementAccompteIS, FicheVerSementTVA,Dirigeants,FicheEffectif,MembreConseil, FicheFiscale,ControleEntreprise, Identification, RegimeFiscale
from rest_framework import routers, serializers, viewsets

class DSFSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSF
        fields = '__all__'


class DADSSerializer (serializers.ModelSerializer):
    class Meta:
        model = DADS
        fields = '__all__'

class ServiceConseilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConseil
        fields = '__all__'

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'

class FormeJuridiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormeJuridique
        fields = '__all__'

class ControleEntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControleEntreprise
        fields = '__all__'

class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = '__all__'

class RegimeFiscaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegimeFiscale
        fields = '__all__'

class FicheFiscaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheFiscale
        fields = '__all__'

class DirigeantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dirigeants
        fields = '__all__'

class MembreConseilSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembreConseil
        fields = '__all__'

class FicheEffectifSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheEffectif
        fields = '__all__'

class FicheVerSementTVASerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheVerSementTVA
        fields = '__all__'

class FicheVersementAccompteISSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheVersementAccompteIS
        fields = '__all__'

class BalanceSixColonneSYSCohadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSixColonneSYSCohada
        fields = '__all__'

class InformationsAutresSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationsAutres
        fields = '__all__'

class FicheVersementSpontaneIRPPSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheVersementSpontaneIRPP
        fields = '__all__'

class EtatSalaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatSalaire
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
