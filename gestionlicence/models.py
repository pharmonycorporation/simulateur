from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Application(models.Model):
    version = models.CharField(max_length=25)
    
    def __str__(self):
        return self.version

class DeviceType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

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
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.devicetype.name)

class Licence(models.Model):
    key = models.CharField(max_length=200, unique=True)
    pack = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="licence")
    validity = models.CharField(max_length=10)
    isActive = models.BooleanField(default=False)
    isBuy = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}, {}".format(self.pack, self.key)

class Personne(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personne')
    phone = models.CharField(max_length=25)
    packages = models.ManyToManyField(Package, through='MyPackages', related_name="personnes")

    def __str__(self):
        return self.user.username

class MyPackages(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    date_souscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.personne.user.username, self.package.name)

