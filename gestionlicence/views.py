from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SigninForm
from .models import *
from django.http import JsonResponse
from decimal import Decimal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import secrets

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
                key = secrets.token_urlsafe(32)
                if paid == "now":
                    pack = Package.objects.get(pk=int(pack_id))
                    MyPackages.objects.create(personne=pers, package=pack)
                    Licence.objects.create(pack=pack, key=key, user_nbre=pack.user_nber, validity=pack.year_duration)
                    paypal_dict = {
                        "business": "guy.anemena@mbcode.cm",
                        "amount": pack.cost,
                        "item_name": pack.name,
                        "invoice": key,
                        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                        "return": request.build_absolute_uri(reverse('payment_done', args=[key])),
                        "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
                        "custom": "premium_plan",  
                    }

                    form = PayPalPaymentsForm(initial=paypal_dict)

                    return render(request, 'payment.html', {'form': form})
                else :
                    pack = Package.objects.get(pk=int(pack_id))
                    MyPackages.objects.create(personne=pers, package=pack)
                    Licence.objects.create(pack=pack, key=key, user_nbre=pack.user_nber, validity=pack.year_duration)
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
            return redirect('signup')
        messages.error(request, form.errors)
        return redirect('signup')


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
    licence = Licence.objects.get(key=key)
    if licence:
        licence.isBuy = True
        licence.isActive = True
        licence.save()
    return render(request, 'payment_done.html')


def payment_canceled(request):
    return render(request, 'payment_cancelled.html')

def verificationLicence(request, key):

    try:
        licence = Licence.objects.get(key=key)
        if licence.firstConnect == True:
            if licence.active == True:
                if licence.user_nbre > 0:
                    nbre = licence.user_nbre
                    licence.user_nbre = nbre - 1
                    licence.active = True
                    licence.firstConnect = False
                    licence.save()
                    return JsonResponse({"message":"Cle verifier"})
                else:
                    return JsonResponse({"erreur":"Le nomre d'utilisateur est depasse"})
            else:
                return JsonResponse({"erreur":"Cette licence n'est pas activee"})
        else:
            if licence.active == True:
                if licence.user_nbre > 0:
                    nbre = licence.user_nbre
                    licence.user_nbre = nbre - 1
                    licence.active = True
                    licence.firstConnect = False
                    licence.save()
                    return JsonResponse({"message":"Cle verifier"})
                else:
                    return JsonResponse({"erreur":"Le nomre d'utilisateur est depasse"})
            else:
                return JsonResponse({"erreur":"Cette licence n'est pas activee"})
    except:
        JsonResponse({"erreur":"Cette cle n'est pas valable"})
