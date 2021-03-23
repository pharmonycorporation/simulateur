from django.db import models
from gestionlicence.models import Personne

class ModePaiement(models.Model):
    mode  = models.CharField(max_length=255, unique=True)
    class Meta:
        ordering: ['-mode']

    def __str__(self):
        return self.mode
class RegimeFiscale(models.Model):
    regime  = models.CharField(max_length=255, unique=True)
    class Meta:
        ordering: ['-regime']

    def __str__(self):
        return self.regime

class MoyenTransport(models.Model):
    moyen  = models.CharField(max_length=255, unique=True)
    class Meta:
        ordering: ['-moyen']

    def __str__(self):
        return self.moyen

class Devise(models.Model):
    nomDevise  = models.CharField(max_length=255,unique=True)
    codeDevise  = models.CharField(max_length=255)
    numeroDevise  = models.IntegerField()
    valeurDevise  = models.IntegerField(default=0)
    class Meta:
        ordering: ['-nomDevise']

    def __str__(self):
        return self.codeDevise
   

class Pays(models.Model):
    nom  = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255)
    cemac = models.BooleanField(default=False)
    africa = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    tva =  models.FloatField(default=18)
    class Meta:
        ordering: ['-nom']

    def __str__(self):
        return self.nom
   
class Simulation (models.Model):
    importateur = models.CharField(max_length=255, verbose_name="Raison sociale")
    regime = models.ForeignKey(RegimeFiscale, on_delete=models.CASCADE, null=True)
    auteur = models.ForeignKey(Personne, on_delete=models.CASCADE, null=True)
    nomenclature = models.CharField(max_length=255)
    destination = models.ForeignKey(Pays, related_name="arrivee", on_delete=models.CASCADE, null=True)
    origine = models.ForeignKey(Pays, related_name="depart", on_delete=models.CASCADE, null=True)
    devise = models.ForeignKey(Devise, on_delete=models.CASCADE, null=True)
    modePaiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE, null=True)
    moyenTransport = models.ForeignKey(MoyenTransport, on_delete=models.CASCADE, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering: ['-importateur']

    def __str__(self):
        return self.importateur
    
class TarifDouanier (models.Model):
    nomenclature = models.CharField(max_length=12,unique=True)
    libelleNomenclature = models.CharField(max_length=255)
    quotite = models.FloatField(default=0)
    exhonereTVA = models.BooleanField(default=False)
    dacc = models.FloatField(default=0)
    ts = models.FloatField(default=0)
    uniteStatistique = models.CharField(max_length=255)
   
    class Meta:
        ordering: ['-nomenclature']

    def __str__(self):
        return self.nomenclature

class TVA (models.Model):
    pays = models.CharField(max_length=255,unique=True)
    valeur = models.FloatField(default=18)
   
    class Meta:
        ordering: ['-pays']

    def __str__(self):
        return self.pays
