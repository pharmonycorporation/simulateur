from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('',home),
    path('signin', signin, name="signin"),
    path('signup', signup, name="signup"),
]