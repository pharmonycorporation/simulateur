from django.db import models

# Create your models here.

class Pays(models.Model):
    nom = models.CharField(max_length=255)

    class Meta:
            ordering: ['-nom']

    def __str__(self):
        return self.nom

class FormeJuridique(models.Model):
    forme = models.CharField(max_length=255)
    
    class Meta:
            ordering: ['-forme']

    def __str__(self):
        return self.forme

class ControleEntreprise(models.Model):
    controle = models.CharField(max_length=255)
    class Meta:
            ordering: ['-controle']

    def __str__(self):
        return self.controle

class Identification (models.Model):
    denominationSociale = models.CharField(max_length=255)
    sigleUsuel = models.CharField(max_length=255)
    adresseComplete = models.CharField(max_length=255, null=True, blank=True)
    boitePostale = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    telecopie = models.CharField(max_length=255, null=True, blank=True)
    nombreEts = models.CharField(max_length=255, null=True, blank=True)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, null=True)
    formeJuridique = models.ForeignKey(FormeJuridique, on_delete=models.CASCADE, null=True)
    controleEntreprise = models.ForeignKey(ControleEntreprise, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)

    class Meta:
            ordering: ['-denominationSociale']

    def __str__(self):
        return self.denominationSociale
    


class RegimeFiscale (models.Model):
    regime = models.CharField(max_length=255)

class FicheFiscale (models.Model):
    numIdentificationFiscale =  models.CharField(max_length=255)
    regimeFiscale = models.ForeignKey(RegimeFiscale, on_delete=models.CASCADE, null=True)
    greffe = models.CharField(max_length=255)
    #sigleUsuel = models.CharField(max_length=255)
    rccm = models.CharField(max_length=255)
    numCodeImportateur = models.CharField(max_length=255)
    numCaisseSociale  = models.CharField(max_length=255)
    dateDebutExercice = models.DateField()
    dateArretComptes = models.DateField()
    dateFinExercice = models.DateField()
    republique = models.CharField(max_length=255)
    ministere = models.CharField(max_length=255)
    direction = models.CharField(max_length=255)
    centre = models.CharField(max_length=255)
    class Meta:
            ordering: ['-numIdentificationFiscale']

    def __str__(self):
        return self.numIdentificationFiscale

class Dirigeants (models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    qualite = models.CharField(max_length=255)
    numIdentificationFiscale = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    class Meta:
        ordering: ['-numIdentificationFiscale']

    def __str__(self):
        return self.nom

class MembreConseil (models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    qualite = models.CharField(max_length=255)
    numIdentificationFiscale = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)

    class Meta:
        ordering: ['-nom']

    def __str__(self):
        return self.nom

class FicheEffectif(models.Model):
    personnelPropre = models.FileField(upload_to = 'documents/')
    personnelExterieur = models.FileField(upload_to = 'documents/')

class FicheVerSementTVA(models.Model):
    document = models.FileField(upload_to = 'documents/')

class FicheVersementAccompteIS(models.Model):
    document = models.FileField(upload_to = 'documents/')

class BalanceSixColonneSYSCohada(models.Model):
    document = models.FileField(upload_to = 'documents/')
   

class InformationsAutres (models.Model):
    nomAdresseQualite = models.CharField(max_length=255)
    nomProfessionnel = models.CharField(max_length=255)
    nomAdresseCommissaireCompte = models.CharField(max_length=255)
    nomSignataireEtatsFinanciers = models.CharField(max_length=255)
    qualiteSignataire = models.CharField(max_length=255)
    dirigeants = models.ManyToManyField(Dirigeants,related_name='informations')
    membresConseil = models.ManyToManyField(MembreConseil,related_name='informations')
    class Meta:
        ordering: ['-nomAdresseQualite']

    def __str__(self):
        return self.nomAdresseQualite

class DSFFile (models.Model):
    ficheVersementTVA = models.FileField(upload_to = 'tva/',null=True)
    ficheVersementAccompteIS = models.FileField(upload_to = 'is/',null=True)
    balanceSixColonneSYSCohada = models.FileField(upload_to = 'syscohoda/',null=True)
    personnelPropre = models.FileField(upload_to = 'ficheeffectif/',null=True)
    personnelExterieur = models.FileField(upload_to = 'ficheeffectif/',null=True)

class DSF (models.Model):
    identification = models.ForeignKey(Identification, on_delete=models.CASCADE, null=True)
    ficheFiscale = models.ForeignKey(FicheFiscale, on_delete=models.CASCADE, null=True)
    infos = models.ForeignKey(InformationsAutres, on_delete=models.CASCADE, null=True)
    dsfFile = models.ForeignKey(DSFFile, on_delete=models.CASCADE, null=True)
    dateSoumission = models.DateTimeField(auto_now_add=True)
    etat = models.BooleanField(default=False)
    paye = models.BooleanField(default=False)
    
    class Meta:
        ordering: ['-dateSoumission']

    def __str__(self):
        return self.identification.denominationSociale 
    

class FicheVersementSpontaneIRPP (models.Model):
    document = models.FileField(upload_to = 'documents/')

class EtatSalaire (models.Model):
    document = models.FileField(upload_to = 'documents/')

class DADSFile(models.Model):
    ficheVersementSpontaneIRPP = models.FileField(upload_to = 'versements/',null=True)

class DADS (models.Model):
    ficheFiscale = models.ForeignKey(FicheFiscale, on_delete=models.CASCADE, null=True)
    dadsFile = models.ForeignKey(DADSFile, on_delete=models.CASCADE, null=True)
    identification = models.ForeignKey(Identification, on_delete=models.CASCADE, null=True)
    etatsSalaires = models.ManyToManyField(EtatSalaire, related_name='dads')
    dateSoumission = models.DateTimeField(auto_now_add=True)
    etat = models.BooleanField(default=False)
    paye = models.BooleanField(default=False)
    
    class Meta:
        ordering: ['-dateSoumission']

    def __str__(self):
        return self.identification.denominationSociale 

class Service (models.Model):
    nomService = models.CharField(max_length=255)
    coutService = models.CharField(max_length=255)
    delai =models.CharField(max_length=255)

class ServiceConseil(models.Model):
    email_contact = models.EmailField(null=True, blank=True)
    objetService = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField()
    dateSoumission = models.DateTimeField(auto_now_add=True)
    etat = models.BooleanField(default=False)
    paye = models.BooleanField(default=False)
    
    class Meta:
        ordering: ['-dateSoumission']

    def __str__(self):
        return self.identification.denominationSociale 
    

   


