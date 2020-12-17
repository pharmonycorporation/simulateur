from django.shortcuts import render
from .serializers import ServiceConseilSerializer, DSFSerializer, DADSSerializer
from .models import DSF, DADS, ServiceConseil
from rest_framework import routers, serializers, viewsets
# Create your views here.

class DSFViewSet(viewsets.ModelViewSet):
    queryset = DSF.objects.all()
    serializer_class = DSFSerializer

class DADSViewSet(viewsets.ModelViewSet):
    queryset = DADS.objects.all()
    serializer_class = DADSSerializer

class ServiceConseilViewSet(viewsets.ModelViewSet):
    queryset = ServiceConseil.objects.all()
    serializer_class = ServiceConseilSerializer