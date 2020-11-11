from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, 'account/signin.html')

def signup(request):
    return render(request, 'account/signup.html')
