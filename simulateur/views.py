from django.shortcuts import render, redirect
from .serializers import TarifDouanierSerializer
import csv
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.core import serializers
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SigninForm, ContactForm
from .models import *
from gestionlicence.models import *
from decimal import Decimal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import secrets
from django.conf import settings 
from django.core.mail import send_mail 
import re
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import get_template, render_to_string
from fpdf import FPDF, HTMLMixin
import math


# -*- coding: utf-8 -*-
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

def initialisationPays(request):
    with open('paysTVA.csv', newline='') as csvfile:
        lecture = csv.reader(csvfile, delimiter=';' )
        for row in lecture:
            if row[1] == 1 :
                cemac = True
            else:
                cemac = False
            pays = Pays.objects.create(nom=row[0],code=row[3],cemac=cemac,tva=float(row[2]))
            pays.save()

def initialisationMonaie(request):
    with open('monnaie.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';' )
        for row in spamreader:
            devise = Devise.objects.create(nomDevise=row[0],codeDevise=row[1],numeroDevise=row[2])
            devise.save()


def suppression(request):
    liste = TarifDouanier.objects.all()
    for tarif in liste:
        tarif.delete()

def ajuster(request):
    liste = TarifDouanier.objects.all()
    for tarif in liste:
        if (re.search("^8703.23.10",tarif.nomenclature)or re.search("^8703.32.10",tarif.nomenclature)):
            tarif.dacc = 25
            tarif.ts = 20
            tarif.save()
        if (re.search("^3917",tarif.nomenclature)or re.search("^3923",tarif.nomenclature)or re.search("^3924",tarif.nomenclature)or re.search("^3926",tarif.nomenclature)):
            tarif.ts = 10
            tarif.save()
     
      

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
       
def home(request):
    if request.user.is_authenticated:       
        return render(request, 'simulateur/home.html')
    return redirect('authentication')
def index(request):
    if request.user.is_authenticated:
        listePays = Pays.objects.all()
        listeRegime = RegimeFiscale.objects.all()
        listePaysCemac = Pays.objects.filter(cemac=True)
        listeTransport = MoyenTransport.objects.all()
        listePaiement = ModePaiement.objects.all()
        listetarif = TarifDouanier.objects.all()
        listeDevise = Devise.objects.all()
        
        return render(request, 'simulateur/index.html', {'tarifs' : listetarif, 'pays':listePays,'cemacs':listePaysCemac, 'transports':listeTransport, 'paiements':listePaiement,'devises':listeDevise,'regimes':listeRegime})
    return redirect('authentication')
    
def tecView(request):
    if request.user.is_authenticated:
        
        listetarif = TarifDouanier.objects.all()
        
        return render(request, 'simulateur/tec.html', {'tarifs' : listetarif})
    return redirect('authentication')

def getProduits(request):
    tarifs = TarifDouanier.objects.all() 
    data = []  
    for tarif in tarifs:
        if tarif.exhonereTVA == True:
            tva = "Oui"
        else:
            tva = "Non"
        objet = {
            "id":tarif.id,
            "nomenclature":tarif.nomenclature,
            "libelleNomenclature":tarif.libelleNomenclature,
            "quotite":tarif.quotite,
            "ts":tarif.ts,
            "tva":tva,
            "dacc":tarif.dacc,
            "uniteStatistique":tarif.uniteStatistique,
             }
        data.append(objet)
    return  JsonResponse(data,safe=False)

def demarrerSimulateur(request):
    importateur = request.POST.get('importateur', None)
    regime = request.POST.get('regime', None)
    destination = request.POST.get('destination', None)
    devise = request.POST.get('devise', None)
    provenance = request.POST.get('provenance', None)
    paiement = request.POST.get('paiement', None)
    transport = request.POST.get('transport', None)
    nomenclature = request.POST.get('nomenclature', None)
    user = User.objects.get(username=request.POST.get('username'))
    #Simulation.objects.create(importateur=importateur,regimeFiscale=regime,destination=Pays.objects.get(nom=destination),origine=Pays.objects.get(nom=provenance),modePaiement=ModePaiement.objects.get(mode=paiement),devise=Devise.objects.get(nomDevise=devise),moyenTransport=MoyenTransport.objects.get(moyen=transport))
    try:
        Simulation.objects.create(importateur=importateur, auteur=Personne.objects.get(user=user), nomenclature=nomenclature,regime=RegimeFiscale.objects.get(regime=regime),destination=Pays.objects.get(nom=destination),origine=Pays.objects.get(nom=provenance),modePaiement=ModePaiement.objects.get(mode=paiement),devise=Devise.objects.get(nomDevise=devise),moyenTransport=MoyenTransport.objects.get(moyen=transport))
        monPays = Pays.objects.get(nom=destination)
        data = {
        'success': True,
        'tva': monPays.tva
        }
   
    except:
        data = {
        'success': False,
        'tva':18
        }
   
    return JsonResponse(data,safe=False)

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

class SignInView(View):
    form_class_to = SignUpForm
    form_class = SigninForm
    template_name = 'simulateur/signin.html'

    def get(self, request, *args, **kwargs):
        form_to = self.form_class_to()
        form = self.form_class()
        return render(request, self.template_name, {'form': form,'form_to':form_to})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form_to = self.form_class_to()
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username,  password=password)
        if user:
            login(request, user)
            return redirect('sdi')
        messages.error(request, "Vos informations de connexion ne sont pas correctes")
        return render(request, self.template_name, {'form': form,'form_to':form_to})

class SignupView(View):
    form_class_to = SigninForm
    form_class = SignUpForm
    template_name = 'simulateur/signin.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form_to = self.form_class_to()
        if form.is_valid():
            usr_email = User.objects.filter(username=form.cleaned_data['email']).exists()
            if usr_email:
                response = {
                    'success' : False,
                    'status_code' : "Errors",
                    'message': "Cet email est déja attribué à un utilisateur !",
                }
            usr = form.save(commit=False)
            usr.is_active = True
            usr.username = form.cleaned_data['email']
            usr.save()
            if usr:
                Personne.objects.create(
                    phone = form.cleaned_data['phone'],
                    user = usr,
                )
            login(request, usr)
            return redirect('sdi')
        messages.error(request, form.errors)
        return redirect('authentication')

class ProfileView(View):
    
    def get(self, request):
        usr = request.user
        #profile = usr.personne
        profile = Personne.objects.get(user=usr)
        nbre = Simulation.objects.filter(auteur=profile).count()
        simulations = None
        if profile:      
            simulations = Simulation.objects.filter(auteur=profile)
        return render(request, 'simulateur/profile.html', {'profile' : profile, 'simulations':simulations, 'nombre':nbre})
    
    def post(self, request):
        change = request.POST.get('change')
        if change == "1":
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            
            usr = User.objects.filter(pk=int(request.user.pk)).update(username=username, first_name=first_name, last_name=last_name)
            if phone:
                pers = Personne.objects.get(user=request.user)
                pers.phone = phone
                pers.save()
            return redirect("up_profile")
        
        elif change == "2":
            currentpassword= request.user.password #user's current password

            oldpass = request.POST.get('oldpassword')
            newpass = request.POST.get('newpassword')
            confirmpass = request.POST.get('confirmpassword')
            
            if newpass == confirmpass:
                
                matchcheck= check_password(oldpass, currentpassword)
            
                if matchcheck:
                    password = make_password(newpass)
                    usr = User.objects.filter(pk=int(request.user.pk)).update(password=password)
                    
                    return redirect("sdi")
                else:
                    messages.error(request, "Votre ancien mot de passe est incorrect")
                    return redirect("up_profile")
            else:
                messages.error(request, "Vos mots de passe ne sont pas identiques")
                return redirect("up_profile")
        else:
            messages.error(request, "Veuillez soumettre votre formulaire")
            return redirect("up_profile")

class SimulationView(View):
    template_name = "simulateur/simulations.html"

    def get(self, request, *args, **kwargs):
        pers = Personne.objects.get(user=request.user)
        simulations = Simulation.objects.filter(auteur=pers)
        return render(request, self.template_name, {'simulations': simulations})


class Mail(View):
    
    def post(self, request):
        print(request.POST)
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            nom = form.cleaned_data.get('nom')
            mail = form.cleaned_data.get('email')
            return send(message,senderMail=mail)
        else:
            return JsonResponse({"erreur":"formulaire nom valide"})
