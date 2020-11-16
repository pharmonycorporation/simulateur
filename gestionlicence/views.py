from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SigninForm, ContactForm
from .models import *
from django.http import JsonResponse
from decimal import Decimal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import secrets
from django.conf import settings 
from django.core.mail import send_mail 
import re
#import braintree
import json
from django.conf import settings

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        packs = Package.objects.filter(active=True)
        faqs = Faq.objects.filter(isActive=True)[:3]
        return render(request, self.template_name, {'packs': packs,'faqs':faqs})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        pack_id = request.POST.get('pack')
        paid = request.POST.get('paid')
        if request.user.is_authenticated:
            try:
                pers = Personne.objects.get(user__email=email)
            except Personne.DoesNotExist:
                pers = None
            if pers:
                if paid == "now":
                    key = secrets.token_hex(16)
                    pack = Package.objects.get(pk=int(pack_id))
                    MyPackages.objects.create(personne=pers, package=pack)
                    paypal_dict = {
                        "business": "guy.anemena@mbcode.cm",
                        "amount": pack.cost,
                        "item_name": pack.name,
                        "invoice": key,
                        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                        "return": request.build_absolute_uri(reverse('payment_done', args=[pack.id])),
                        "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
                        "custom": "premium_plan",  
                    }

                    subject = 'commande du pack cgi'
                    message = f'Hi {request.user.username}, merci davoir souscrit a notre pack.'
                    email_from = settings.EMAIL_HOST_USER 
                    recipient_list = [email, ] 
                    send_mail( subject, message, email_from, recipient_list )

                    form = PayPalPaymentsForm(initial=paypal_dict)

                    return render(request, 'payment.html', {'form': form})
                else :
                    pack = Package.objects.get(pk=int(pack_id))
                    MyPackages.objects.create(personne=pers, package=pack)
                    
            return redirect('signin')
        return redirect('signin')

class SignupView(View):
    form_class = SignUpForm
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
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
            return redirect('home')
        messages.error(request, form.errors)
        return redirect('signup')

def achat(request, pk):
    if request.user.is_authenticated:
        
        key = secrets.token_hex(16)
        pack = Package.objects.get(pk=int(pk))
        MyPackages.objects.create(personne=request.user.personne, package=pack)
        taux_conversion = 0.0015
        
        amount = (pack.cost * taux_conversion)

        paypal_dict = {
            "business": "guy.anemena@mbcode.cm",
            "amount": amount,
            "item_name": pack.name,
            "invoice": key,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('payment_done', args=[pk])),
            "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
            "custom": "premium_plan",  
            "currency_code": "EUR"
        }

        """subject = 'commande du pack cgi'
        message = f'Hi {request.user.username}, merci davoir souscrit a notre pack.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [email, ] 
        send_mail( subject, message, email_from, recipient_list )"""

        form = PayPalPaymentsForm(initial=paypal_dict)

        return render(request, 'payment.html', {'form': form})
                
    return redirect('signin')



class SignInView(View):
    form_class = SigninForm
    template_name = 'account/signin.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username,  password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Vos informations de connexion ne sont pas correctes")
        return render(request, self.template_name)

class SouscriptionView(View):
    template_name = "souscriptions.html"

    def get(self, request, *args, **kwargs):
        pers = Personne.objects.get(user=request.user)
        packages = MyPackages.objects.filter(personne=pers)
        return render(request, self.template_name, {'packages': packages})

    def post(self, request, *args, **kwargs):
        pass

def signout(request):
    logout(request)
    return redirect("home")

def payment_done(request, key):
    pack = Package.objects.get(pk=int(key))
    key = secrets.token_urlsafe(32)

    myPack = MyPackages.objects.filter(personne=request.user.personne, package=pack, is_paid=False).first()
    myPack.is_paid = True
    myPack.save()

    Licence.objects.create(pack=pack, key=key, user_nbre=pack.user_nber, validity=pack.year_duration, isBuy=True, isActive=True)
    #envoyer un mail contenant la licence du pack souscrit
    """subject = 'commande du pack cgi'
    message = f'Hi {request.user.username}, merci davoir souscrit a notre pack.'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [email, ] 
    send_mail( subject, message, email_from, recipient_list )"""
    
    return render(request, 'payment_done.html')

def payment_canceled(request):
    return render(request, 'payment_cancelled.html')

def verificationLicence(key):

    try:
        licence = Licence.objects.get(key=str(key))
        if licence.active == True:
            if licence.user_nbre > 0:
                nbre = licence.user_nbre
                licence.user_nbre = nbre - 1
                licence.active = True
                licence.firstConnect = False
                licence.save()
                reponse = dict()
                reponse['message'] = "Cle verifiee"
                version = licence.pack.version.version
                reponse['version'] = version
                return JsonResponse(reponse)
            else:
                return JsonResponse({"erreur":"Le nombre d'utilisateur est depasse"})
        else:
            return JsonResponse({"erreur":"Cette licence n'est pas activee"})
    except:
        return JsonResponse({"erreur":"Cette cle n'est pas valable"})



def send(mailContent, senderMail="kenmognethimotee@gmail.com", subject=''):
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.search(regex,senderMail):
        send_mail(subject=subject,message=mailContent, recipient_list=[senderMail],from_email=settings.EMAIL_HOST_USER)
        return JsonResponse({"message":"mail envoyer"})
    else:
        return JsonResponse({"erreur":"Mail invalid"})


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


class LicenceView(View):

    def get(self, request, key):
        #key = request.POST['key']
        return verificationLicence(key)

class LatestVersion(View):

    def get(self, request):

        try:
            application = Application.objects.latest('version')
            version = application.version
            fichier_url = application.archive.url

            return JsonResponse({"version":version, "fichier":fichier_url})
        except:
            return JsonResponse({"erreur":"Pas de derniere version"})


class Contact(View):


    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            pass
        else:
            pass
