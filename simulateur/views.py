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
        x = tarif.nomenclature.split(".")
        if re.search("^0402", x[0]) or re.search("^05", x[0]) or re.search("^4902", x[0]) or re.search("^31", x[0]):
            tarif.exhonereTVA = True
            tarif.save() 

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
