from django.urls import path, include
from .models import TarifDouanier
from rest_framework import routers, serializers, viewsets



class TarifDouanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifDouanier
        fields = '__all__'