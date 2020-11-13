from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Personne)
admin.site.register(Licence)
admin.site.register(Application)
admin.site.register(DeviceType)
admin.site.register(Package)
admin.site.register(MyPackages)
admin.site.register(Faq)
