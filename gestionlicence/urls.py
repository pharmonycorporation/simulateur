from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('',home, name="home"),
    path('signin/', SignInView.as_view(), name="signin"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('logout/', signout, name="signout")
]