from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('signin/', SignInView.as_view(), name="signin"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('souscriptions/', SouscriptionView.as_view(), name="souscriptions"),
    path('logout/', signout, name="signout")
]