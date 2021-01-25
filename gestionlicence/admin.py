from django.contrib import admin
from .models import *

# Register your models here.
class LicenceAdmin(admin.ModelAdmin):
    list_display= ('key', 'user_nbre', 'validity' , 'active','isActive')
    search_fields = ('key',)
    #search_fields = ('nomSeance', )
    #fields = ('nomSeance', 'plage',  'capacite', 'disponible', 'culte', 'dateCreated', 'active')
    list_per_page = 50
    #autocomplete_fields = ['culte']
    #list_display_links = ('nomCulte' )
    actions = ['activer_les_licences']

    def activer_les_licences(self, request, queryset):
    
        #updated = queryset.update(status='p')
        queryset2 = Licence.objects.all()
        for licence in queryset2:
            licence.active = True
            licence.save()
        
        return True
       

admin.site.register(Personne)
admin.site.register(Licence,LicenceAdmin)
admin.site.register(Application)
admin.site.register(DeviceType)
admin.site.register(Package)
admin.site.register(Faq)
admin.site.register(MyPackages)
