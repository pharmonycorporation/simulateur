from django.urls import path, include
from .models import DSF, DADS, DADSFile, DSFFile, ServiceConseil, Pays, FormeJuridique,EtatSalaire, Service, InformationsAutres,FicheVersementSpontaneIRPP, BalanceSixColonneSYSCohada, FicheVersementAccompteIS, FicheVerSementTVA,Dirigeants,FicheEffectif,MembreConseil, FicheFiscale,ControleEntreprise, Identification, RegimeFiscale
from rest_framework import routers, serializers, viewsets



class DSFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSFFile
        fields = '__all__'


class DADSSerializer (serializers.ModelSerializer):
    class Meta:
        model = DADS
        fields = '__all__'

class DADSFileSerializer (serializers.ModelSerializer):
    class Meta:
        model = DADSFile
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
    dirigeants = serializers.PrimaryKeyRelatedField(queryset=Dirigeants.objects.all(), many=True)
    membresConseil = serializers.PrimaryKeyRelatedField(queryset=MembreConseil.objects.all(), many=True)
   
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

class DSFSerializer(serializers.ModelSerializer):
    ficheFiscale =  FicheFiscaleSerializer()
    identification = IdentificationSerializer()
   
    class Meta:
        model = DSF
        fields = '__all__'
    
    def create(self, validate_data):
        ficheFiscale= FicheFiscaleSerializer(data=validate_data.pop('ficheFiscale'))
        identification= IdentificationSerializer(data=validate_data.pop('identification'))
        infos= InformationsAutresSerializer(data=validate_data.pop('infos'))
     
        if infos.is_valid():
            info = infos.save()
        else:
            info = InformationsAutres.objects.create(nomAdresseQualite=infos.data.get('nomAdresseQualite'),nomProfessionnel=infos.data.get('nomProfessionnel'),nomAdresseCommissaireCompte=infos.data.get('nomAdresseCommissaireCompte'),nomSignataireEtatsFinanciers=infos.data.get('nomSignataireEtatsFinanciers'),qualiteSignataire=infos.data.get('qualiteSignataire'))
            print(infos.errors)
        if identification.is_valid():
            ident = identification.save()
            
        else:
            ident = Identification.objects.create(denominationSociale=identification.data.get('denominationSociale'),sigleUsuel=identification.data.get('sigleUsuel'),adresseComplete=identification.data.get('adresseComplete'),boitePostale=identification.data.get('boitePostale'),ville=identification.data.get('ville'),telephone=identification.data.get('telephone'),telecopie=identification.data.get('telecopie'),nombreEts=identification.data.get('nombreEts'),active=True,pays=identification.data.get('pays'),formeJuridique=identification.data.get('formeJuridique'),controleEntreprise=identification.data.get('controleEntreprise'))
            #print(identification.errors)
        if ficheFiscale.is_valid():
            fiche = ficheFiscale.save()
        else:
            fiche = FicheFiscale.objects.create(numIdentificationFiscale=ficheFiscale.data.get('numIdentificationFiscale'),greffe=ficheFiscale.data.get('greffe'),rccm=ficheFiscale.data.get('rccm'),numCodeImportateur=ficheFiscale.data.get('numCodeImportateur'),numCaisseSociale=ficheFiscale.data.get('numCaisseSociale'),dateDebutExercice=ficheFiscale.data.get('dateDebutExercice'),dateArretComptes=ficheFiscale.data.get('dateArretComptes'),dateFinExercice=ficheFiscale.data.get('dateFinExercice'),republique=ficheFiscale.data.get('republique'),ministere=ficheFiscale.data.get('ministere'),direction=ficheFiscale.data.get('direction'),centre=ficheFiscale.data.get('centre'),regimeFiscale=ficheFiscale.data.get('regimeFiscale'))
            #print(ficheFiscale.errors)
        return DSF.objects.create(identification = ident,ficheFiscale=fiche, infos=info, **validate_data)
