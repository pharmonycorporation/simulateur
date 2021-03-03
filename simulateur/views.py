from django.shortcuts import render
from .models import TarifDouanier
from .serializers import TarifDouanierSerializer
import csv
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.core import serializers

def initialisationTarif(request):
    with open('tarifdouanier.csv', newline='') as csvfile:
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

def index(request):
    
    listetarif = TarifDouanier.objects.all()
    return render(request, 'simulateur/index.html', {'tarifs' : listetarif })

def getProd(request):
    id = request.GET.get('id', None)
    #data = TarifDouanierSerializer(TarifDouanier.object.get(pk=id))
    data = {
    'is_not_in': TarifDouanier.objects.filter(id__iexact=id).exists()
    }
    prod =TarifDouanier.objects.get(pk=id)
    objet = {
        "id":prod.id,
        "nomenclature":prod.nomenclature,
        "libelleNomenclature":prod.libelleNomenclature,
        "quotite":prod.quotite,
        "ts":prod.ts,
        "uniteStatistique":prod.uniteStatistique,
        
    }
    data['tarif']=objet
    #prod = TarifDouanier.get(id=id)
    if data['is_not_in']:
        pass
    else:
        data['error_message'] = "Cette clé n'existe pas."
  
    return  JsonResponse(data,safe=False)