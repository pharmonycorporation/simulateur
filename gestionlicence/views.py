from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SigninForm
from .models import *

# Create your views here.


def home(request):
    return render(request, 'index.html')

class SignupView(View):
    form_class = SignUpForm
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            usr_email = User.objects.filter(email=form.cleaned_data['email']).exists()
            if usr_email:
                response = {
                    'success' : False,
                    'status_code' : "Errors",
                    'message': "Cet email est déja attribué à un utilisateur !",
                }
            usr = form.save(commit=False)
            usr.is_active = True
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
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username,  password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, self.template_name)

class ValidateEmail(View):
    pass

def signout(request):
    logout(request)
    return redirect("home")
