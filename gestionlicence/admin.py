from django.contrib import admin
from .models import *
from .views import HtmlPdf
from django.template.loader import get_template, render_to_string
from fpdf import FPDF, HTMLMixin
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponse
from decimal import Decimal
from django.urls import reverse

# Register your models here.
class LicenceAdmin(admin.ModelAdmin):
    list_display= ('key', 'user_nbre', 'validity' , 'active','isActive')
    search_fields = ('key',)
    #search_fields = ('nomSeance', )
    #fields = ('nomSeance', 'plage',  'capacite', 'disponible', 'culte', 'dateCreated', 'active')
    list_per_page = 50
    #autocomplete_fields = ['culte']
    #list_display_links = ('nomCulte' )
    actions = ['activer_les_licences','liste_licences_pdf_non_utilise']

    def activer_les_licences(self, request, queryset):
    
        #updated = queryset.update(status='p')
        queryset2 = Licence.objects.all()
        for licence in queryset2:
            licence.active = True
            licence.save()
        
        return True

    def liste_licences_pdf_non_utilise(self, request, queryset):    
        pdf = HtmlPdf()
        pdf.add_page()
        licences = []
        licences = Licence.objects.filter(isActive=False)
        pdf.write_html(render_to_string('pdfob.html', {'licences': licences}))
        response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
        response['Content-Type'] = 'application/pdf'
        return response

       

admin.site.register(Personne)
admin.site.register(Licence,LicenceAdmin)
admin.site.register(Application)
admin.site.register(DeviceType)
admin.site.register(Package)
admin.site.register(Faq)
admin.site.register(MyPackages)
