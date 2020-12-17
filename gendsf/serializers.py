from django.urls import path, include
from .models import DSF, DADS, ServiceConseil
from rest_framework import routers, serializers, viewsets

class DSFSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSF
        fields = '__all__'


class DADSSerializer (serializers.ModelSerializer):
    class Meta:
        model = DADS
        fields = '__all__'

class ServiceConseilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConseil
        fields = '__all__'
