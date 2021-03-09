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
        if (re.search("^2202",tarif.nomenclature)):
            tarif.dacc = 10
        if (re.search("^2203",tarif.nomenclature)):
            tarif.dacc = 25
            tarif.ts= 10
        if (re.search("^2204",tarif.nomenclature) or re.search("^2205",tarif.nomenclature)):
            tarif.dacc = 25
            tarif.ts= 15
        if (re.search("^2204",tarif.nomenclature)):
            tarif.dacc = 25
            tarif.ts= 20

        """if (re.search("^8501.10.00", tarif.nomenclature) or re.search("^8541.40.00", tarif.nomenclature)or re.search("^8504.31.00", tarif.nomenclature) or re.search("^8504.40.00", tarif.nomenclature) or re.search("^9030.39.00", tarif.nomenclature) or
           re.search("^8544.20.00", tarif.nomenclature) or re.search("^8507.80.00", tarif.nomenclature) or re.search("^8536.30.00", tarif.nomenclature) or 
           re.search("^8507.80.00", tarif.nomenclature) or re.search("^8504.90.00", tarif.nomenclature) or re.search("^8513.10.00", tarif.nomenclature) or  
           re.search("^8513.10.00", tarif.nomenclature) or re.search("^8436.80.00", tarif.nomenclature) or re.search("^8413.82.00", tarif.nomenclature) or 
           re.search("^8537.10.00", tarif.nomenclature) or re.search("^8419.40.00", tarif.nomenclature) or re.search("^8419.31.00", tarif.nomenclature) or 
           re.search("^8413.81.00", tarif.nomenclature) or re.search("^8419.31.00", tarif.nomenclature) or re.search("^8504.34.00", tarif.nomenclature) or 
           re.search("^8504.40.00", tarif.nomenclature) or re.search("^9030.39.00", tarif.nomenclature) or re.search("^2836.50.00", tarif.nomenclature) or 
           re.search("^3204", tarif.nomenclature) or re.search("^3901", tarif.nomenclature) or re.search("^3902", tarif.nomenclature) or 
           re.search("^3907.30.00", tarif.nomenclature) or re.search("^3907.50.00", tarif.nomenclature) or re.search("^3909", tarif.nomenclature) or 
           re.search("^3911", tarif.nomenclature) or re.search("^3905", tarif.nomenclature) or re.search("^3906", tarif.nomenclature) or 
           re.search("^3907", tarif.nomenclature) or re.search("^3908", tarif.nomenclature) or re.search("^3915", tarif.nomenclature) or 
           re.search("^8421.21.00", tarif.nomenclature) or re.search("^8412.80.00", tarif.nomenclature) or re.search("^8410", tarif.nomenclature) or  re.search("^8504.33.00", tarif.nomenclature)or  re.search("^8465.99.00", tarif.nomenclature) ): 
           
            
            tarif.exhonereTVA = True
            tarif.save() 

        x = tarif.nomenclature.split(".")"""
       
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
