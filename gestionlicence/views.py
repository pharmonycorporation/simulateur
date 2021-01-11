from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SigninForm, ContactForm
from .models import *
from django.http import JsonResponse
from decimal import Decimal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import secrets
from django.conf import settings 
from django.core.mail import send_mail 
import re
#import braintree
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        packs = Package.objects.filter(active=True)
        faqs = Faq.objects.filter(isActive=True)[:3]
        return render(request, self.template_name, {'packs': packs,'faqs':faqs})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        pack_id = request.POST.get('pack')
        paid = request.POST.get('paid')
        if request.user.is_authenticated:
            try:
                pers = Personne.objects.get(user__email=email)
            except Personne.DoesNotExist:
                pers = None
            if pers:
                if paid == "now":
                    key = secrets.token_hex(16)
                    pack = Package.objects.get(pk=int(pack_id))
                    MyPackages.objects.create(personne=pers, package=pack)
                    paypal_dict = {
                        "business": "guy.anemena@mbcode.cm",
                        "amount": pack.cost,
                        "item_name": pack.name,
                        "invoice": key,
                        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                        "return": request.build_absolute_uri(reverse('payment_done', args=[pack.id])),
                        "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
                        "custom": "premium_plan",  
                    }

                    subject = 'commande du pack cgi'
                    message = f'Hi {request.user.username}, merci davoir souscrit a notre pack.'
                    email_from = settings.EMAIL_HOST_USER 
                    recipient_list = [email, ] 
                    send_mail( subject, message, email_from, recipient_list )

                    form = PayPalPaymentsForm(initial=paypal_dict)

                    return render(request, 'payment.html', {'form': form})
                else :
                    pack = Package.objects.get(pk=int(pack_id))
                    MyPackages.objects.create(personne=pers, package=pack)
                    
            return redirect('signin')
        return redirect('signin')

class SignupView(View):
    form_class = SignUpForm
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            usr_email = User.objects.filter(username=form.cleaned_data['email']).exists()
            if usr_email:
                response = {
                    'success' : False,
                    'status_code' : "Errors",
                    'message': "Cet email est déja attribué à un utilisateur !",
                }
            usr = form.save(commit=False)
            usr.is_active = True
            usr.username = form.cleaned_data['email']
            usr.save()
            if usr:
                Personne.objects.create(
                    phone = form.cleaned_data['phone'],
                    user = usr,
                )
            return redirect('home')
        messages.error(request, form.errors)
        return redirect('signup')

def achat(request, pk):
    if request.user.is_authenticated:
        
        key = secrets.token_hex(16)
        pack = Package.objects.get(pk=int(pk))
        MyPackages.objects.create(personne=request.user.personne, package=pack)
        taux_conversion = 0.0015
        
        amount = (pack.cost * taux_conversion)

        paypal_dict = {
            "business": "guy.anemena@mbcode.cm",
            "amount": amount,
            "item_name": pack.name,
            "invoice": key,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('payment_done', args=[pk])),
            "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
            "custom": "premium_plan",  
            "currency_code": "EUR"
        }

        subject = 'commande du pack cgi'
        message = f'Hi {request.user.username}, merci davoir souscrit a notre pack.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [email, ] 
        send_mail( subject, message, email_from, recipient_list )

        form = PayPalPaymentsForm(initial=paypal_dict)

        return render(request, 'payment.html', {'form': form})
                
    return redirect('signin')



class SignInView(View):
    form_class = SigninForm
    template_name = 'account/signin.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username,  password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Vos informations de connexion ne sont pas correctes")
        return render(request, self.template_name)

class SouscriptionView(View):
    template_name = "souscriptions.html"

    def get(self, request, *args, **kwargs):
        pers = Personne.objects.get(user=request.user)
        packages = MyPackages.objects.filter(personne=pers)
        return render(request, self.template_name, {'packages': packages})

    def post(self, request, *args, **kwargs):
        pass

def signout(request):
    logout(request)
    return redirect("home")

def payment_done(request, key):
    pack = Package.objects.get(pk=int(key))
    key = secrets.token_urlsafe(32)
    email = request.user.email

    myPack = MyPackages.objects.filter(personne=request.user.personne, package=pack, is_paid=False).first()
    myPack.is_paid = True
    myPack.save()

    Licence.objects.create(pack=pack, key=key, user_nbre=pack.user_nber, validity=pack.year_duration, isBuy=True, isActive=True)
    #envoyer un mail contenant la licence du pack souscrit
    subject = 'commande du pack cgi'
    message = f'Hi {request.user.username}, votre clé de licence est :' + key
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [email, ] 
    send_mail( subject, message, email_from, recipient_list )
    
    return render(request, 'index.html')

def payment_canceled(request):
    return render(request, 'payment_cancelled.html')

def verificationLicence(key):

    try:
        licence = Licence.objects.get(key=str(key))
        if licence.active == True:
            if licence.user_nbre > 0:
                nbre = licence.user_nbre
                licence.user_nbre = nbre - 1
                licence.active = True
                licence.firstConnect = False
                licence.save()
                reponse = dict()
                reponse['message'] = "Cle verifiee"
                version = licence.pack.version.version
                reponse['version'] = version
                return JsonResponse(reponse)
            else:
                return JsonResponse({"erreur":"Le nombre d'utilisateur est depasse"})
        else:
            return JsonResponse({"erreur":"Cette licence n'est pas activee"})
    except:
        return JsonResponse({"erreur":"Cette cle n'est pas valable"})



def send(mailContent, senderMail="kenmognethimotee@gmail.com", subject=''):
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.search(regex,senderMail):
        send_mail(subject=subject,message=mailContent, recipient_list=["contact@cgitchad.online"],from_email=settings.EMAIL_HOST_USER)
        return JsonResponse({"message":"mail envoyer"})
    else:
        return JsonResponse({"erreur":"Mail invalid"})


@api_view(['GET', 'POST'])
@csrf_exempt
def envoiMail(request):

    message = request.data.get('message')
    nom = request.data.get('nom')
    mail = request.data.get('email')
    objet = request.data.get('objet')

    return send(message, senderMail=mail, subject=nom+" : "+objet)
    pass

class Mail(View):

    def post(self, request):
        print(request.POST)
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            nom = form.cleaned_data.get('nom')
            mail = form.cleaned_data.get('email')
            return send(message,senderMail=mail)
        else:
            return JsonResponse({"erreur":"formulaire nom valide"})


class LicenceView(View):

    def get(self, request, key):
        #key = request.POST['key']
        return verificationLicence(key)

class LatestVersion(View):

    def get(self, request):

        try:
            application = Application.objects.latest('version')
            version = application.version
            fichier_url = application.archive.url

            return JsonResponse({"version":version, "fichier":fichier_url})
        except:
            return JsonResponse({"erreur":"Pas de derniere version"})


class Contact(View):


    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            pass
        else:
            pass

class ProfileView(View):
    
    def get(self, request):
        usr = request.user
        #profile = usr.personne
        profile = Personne.objects.get(user=usr)
        nbre = MyPackages.objects.filter(personne=profile).count()
        packages = None
        if profile:      
            packages = MyPackages.objects.filter(personne=profile)
        return render(request, 'account/profile.html', {'profile' : profile, 'packages':packages, 'nbre_packages':nbre})
    
    def post(self, request):
        change = request.POST.get('change')
        if change == "1":
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            
            usr = User.objects.filter(pk=int(request.user.pk)).update(username=username, first_name=first_name, last_name=last_name)
            if phone:
                pers = Personne.objects.get(user=request.user)
                pers.phone = phone
                pers.save()
            return redirect("profile")
        
        elif change == "2":
            currentpassword= request.user.password #user's current password

            oldpass = request.POST.get('oldpassword')
            newpass = request.POST.get('newpassword')
            confirmpass = request.POST.get('confirmpassword')
            
            if newpass == confirmpass:
                
                matchcheck= check_password(oldpass, currentpassword)
            
                if matchcheck:
                    password = make_password(newpass)
                    usr = User.objects.filter(pk=int(request.user.pk)).update(password=password)
                    
                    return redirect("home")
                else:
                    messages.error(request, "Votre ancien mot de passe est incorrect")
                    return redirect("profile")
            else:
                messages.error(request, "Vos mots de passe ne sont pas identiques")
                return redirect("profile")
        else:
            messages.error(request, "Veuillez soumettre votre formulaire")
            return redirect("profile")


class HtmlPdf(FPDF, HTMLMixin):
    
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)

def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(math.sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True

def hash_key():
    key = secrets.token_hex(3)
    print(key)
    key1 = key.upper()
    hexa = 0
    for el in key.upper():
        print(int(el, 16))
        hexa = hexa + int(el, 16)
    est_premier = is_prime(hexa)
    if est_premier:
        second_hexa = hex(hexa)
        test = second_hexa.replace("0x","")
    else:
        add_hexa = hexa
        i = hexa
        while not is_prime(i):
            i += 1
        first_test = i + add_hexa
        second_hexa = hex(first_test)
        test = second_hexa.replace("0x","")
    if len(str(test)) < 4:
        nbre = 4 - int(len(str(test)))
        keygen = secrets.token_hex(nbre)
        key2 = keygen.upper() + test.upper()
    else:
        key2 = test
    hexa3 = 0
    for el in key2:
        print(int(el, 16))
        hexa3 = hexa3 + int(el, 16)
    print(hexa3)
    premier = is_prime(hexa3)
    if premier:
        third_hexa = hex(hexa3)
        test2 = third_hexa.replace("0x","")
    else:
        add_hexa2 = hexa3
        i = hexa
        while not is_prime(i):
            i += 1
        second_test = i + add_hexa2
        third_hexa = hex(second_test)
        test2 = third_hexa.replace("0x","")
    if len(str(test2)) < 4:
        nbre2 = 4 - int(len(str(test2)))
        keygen2 = secrets.token_hex(nbre2)
        key3 = keygen2.upper() + test2.upper()
    else:
        key3 = test2
    
    cle = key1 + '-' + key2 + '-' + key3
    print(cle)
    return cle

def print_pdf(request):    
    pdf = HtmlPdf()
    pdf.add_page()
    licences = []
    for i in range(500):
        pack = Package.objects.get(pk=int(1))
        cle = hash_key()
        key = hash_key().replace('-', '')
        Licence.objects.create(pack=pack, key=key, user_nbre=1, validity=pack.year_duration, isBuy=True, isActive=True)
        licences.append(cle)
    """pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.cell(60, 10, 'Powered by FPDF.', 0, 1, 'C')
    pdf.output('tuto1.pdf', 'F')"""
    pdf.write_html(render_to_string('pdf.html', {'licences': licences}))
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response


def page_not_found(request,HttpResponseNotFound):
    return render(request, '404.html')

def server_error(request,**kwargs):
    return render(request, '500.html')

