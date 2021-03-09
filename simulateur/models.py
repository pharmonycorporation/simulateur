from django.db import models

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
