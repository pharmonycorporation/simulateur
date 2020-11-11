from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Personne(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personne')
    phone = models.CharField(max_length=25)

    def __str__(self):
        return self.phone

class Licence(models.Model):
    key = models.CharField(max_length=200, unique=True)
    validity = models.CharField(max_length=10)
    isActive = models.BooleanField(default=False)
    isBuy = models.BooleanField(default=False)

    def __str__(self):
        return self.key

class Application(models.Model):
    version = models.CharField(max_length=25)
    
    def __str__(self):
        return self.version

class DeviceType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user_nber = models.IntegerField(default=0)
    year_duration = models.IntegerField(default=0)
    performance = models.CharField(max_length=255, null=True, blank=True)
    cost = models.FloatField(default=0)
    devicetype = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    licence_key = models.OneToOneField(Licence, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(self.name, self.devicetype.name)

