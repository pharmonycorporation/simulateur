from django.shortcuts import render
from .models import TarifDouanier, TVA
from .serializers import TarifDouanierSerializer
import csv
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.core import serializers
import re

def initialisationTarif(request):
    with open('tarif2.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';' )
        for row in spamreader:
            if isinstance(row[2], (int,float)):
                quotite = row[2]
            else:
                quotite = int(row[2]) if int(row[2]) else 0
            tarif = TarifDouanier.objects.create(nomenclature=row[0],libelleNomenclature=row[1],quotite=quotite,uniteStatistique=row[3])
            tarif.save()


def suppression(request):
    liste = TarifDouanier.objects.all()
    for tarif in liste:
        tarif.delete()

def ajuster(request):
    liste = TarifDouanier.objects.all()
    for tarif in liste:

        if (re.search("^4901.91.00", tarif.nomenclature) or re.search("^1001.10.10", tarif.nomenclature)or re.search("^1002.00.10", tarif.nomenclature) or re.search("^1004.00.10", tarif.nomenclature) or re.search("^1005.10.00", tarif.nomenclature) or
           re.search("^0511.10.00", tarif.nomenclature) or re.search("^0407.11.00", tarif.nomenclature) or re.search("^8414.60.00", tarif.nomenclature) or 
           re.search("^8419.31.00", tarif.nomenclature) or re.search("^8716.80.10", tarif.nomenclature) or re.search("^8436.10.00", tarif.nomenclature) or  
           re.search("^8445.19.10", tarif.nomenclature) or re.search("^8479.82.00", tarif.nomenclature) or re.search("^8479.82.00", tarif.nomenclature) or 
           re.search("^8476.89.00", tarif.nomenclature) or re.search("^8436.21.00", tarif.nomenclature) or re.search("^8705.90.00", tarif.nomenclature) or 
           re.search("^8436.21.00", tarif.nomenclature) or re.search("^8436.10.00", tarif.nomenclature) or re.search("^8504.21", tarif.nomenclature) or  re.search("^8504.23", tarif.nomenclature) ): 
           
            
            tarif.exhonereTVA = True
            tarif.save() 

        x = tarif.nomenclature.split(".")
       
def index(request):
    
    listetarif = TarifDouanier.objects.all()
    tva = TVA.objects.all()
    return render(request, 'simulateur/index.html', {'tarifs' : listetarif, 'tvas' :tva })

def getProd(request):
    id = request.GET.get('id', None)
    #data = TarifDouanierSerializer(TarifDouanier.object.get(pk=id))
    data = {
    'is_not_in': TarifDouanier.objects.filter(id__iexact=id).exists()
    }
    prod =TarifDouanier.objects.get(pk=id)
    if prod.exhonereTVA == True:
        tva = 0
    else:
        tva = 1
    objet = {
        "id":prod.id,
        "nomenclature":prod.nomenclature,
        "libelleNomenclature":prod.libelleNomenclature,
        "quotite":prod.quotite,
        "ts":prod.ts,
        "tva":tva,
        "dacc":prod.dacc,
        "uniteStatistique":prod.uniteStatistique,
        
    }
    data['tarif']=objet
    #prod = TarifDouanier.get(id=id)
    if data['is_not_in']:
        pass
    else:
        data['error_message'] = "Cette clé n'existe pas."
  
    return  JsonResponse(data,safe=False)
