from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SigninForm
from .models import *
from django.http import JsonResponse

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
        print('my email address')
        print(email)
        if email:
            try:
                pers = User.objects.get(username=email)
            except User.DoesNotExist:
                pers = None
            print(pers)
            if pers:
                pack = Package.objects.get(pk=int(pack_id))
                pass
            print('user personne does not exist')
        print('you dont send email address')

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
            return render(request, self.template_name)
        pass


class SignInView(View):
    form_class = SigninForm
    template_name = 'account/signin.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        username = form["email"].value()
        password = form["password"].value()
        user = authenticate(request, username=username,  password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, self.template_name)

class SouscriptionView(View):
    template_name = "souscriptions.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        pers = usr.personne
        print(pers)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

def signout(request):
    logout(request)
    return redirect("home")



def verificationLicence(request, key):

    try:
        licence = Licence.objects.get(key=key)
        if licence.firstConnect == True:
            if licence.active = True:
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
            if licence.active = True:
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
        JsonResponse({"erreur":"Cette cle n'est pas valable")
