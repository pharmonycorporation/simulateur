from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SigninForm
from .models import *
from decimal import Decimal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        packs = Package.objects.filter(active=True)
        return render(request, self.template_name, {'packs': packs})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        pack_id = request.POST.get('pack')
        if email:
            try:
                pers = Personne.objects.get(user__email=email)
            except Personne.DoesNotExist:
                pers = None
            if pers:
                pack = Package.objects.get(pk=int(pack_id))
                MyPackages.objects.create(personne=pers, package=pack)
                paypal_dict = {
                    "business": "guy.anemena@mbcode.cm",
                    "amount": pack.cost,
                    "item_name": pack.name,
                    "invoice": "112556568968",
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": request.build_absolute_uri(reverse('home')),
                    "cancel_return": request.build_absolute_uri(reverse('home')),
                    "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
                }

                form = PayPalPaymentsForm(initial=paypal_dict)

                return render(request, 'payment.html', {'form': form})
            return redirect('home')
        return redirect('home')

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
        pers = Personne.objects.get(user=request.user)
        packages = MyPackages.objects.filter(personne=pers)
        print('list pakages')
        print(packages)
        return render(request, self.template_name, {'packages': packages})

    def post(self, request, *args, **kwargs):
        pass

def signout(request):
    logout(request)
    return redirect("home")