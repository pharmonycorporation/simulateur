from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('signin/', SignInView.as_view(), name="signin"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('souscriptions/', SouscriptionView.as_view(), name="souscriptions"),
    path('logout/', signout, name="signout"),
    path('achat/<int:pk>', achat, name="achat"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('payment-done/<str:key>', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
    path('verification/<str:key>', LicenceView.as_view(), name='verification'),
    path('envoimail/', envoiMail, name='mail'),
    path('latestversion/', LatestVersion.as_view(), name='latest'),
    path('pdf/', web_views.print_pdf, name='licence'),
    path('test/', hash_key, name='test'),
]