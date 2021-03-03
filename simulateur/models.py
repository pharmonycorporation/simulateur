from django.db import models

class TarifDouanier (models.Model):
    nomenclature = models.CharField(max_length=12,unique=True)
    libelleNomenclature = models.CharField(max_length=255)
    quotite = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    uniteStatistique = models.CharField(max_length=255)
   
    class Meta:
        ordering: ['-nomenclature']

    def __str__(self):
        return self.nomenclature
