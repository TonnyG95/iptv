from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from korisnici.models import Novcanik, UserProfile, Subscription, UserSubscription, KategorijaKanala, Kanal, KontaktPoruka, Announcement
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
import os
from django.conf import settings
from django.utils.html import strip_tags
from django.http import JsonResponse
import paypalrestsdk
import json
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from korisnici.management.commands.dnevna_provjera_preplata import provjeri_istek_preplata
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist


def is_admin(user):
    return user.is_staff


def registracija(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        if not User.objects.filter(email=email).exists():
            new_user = User.objects.create_user(username=email, password=password,
                                                first_name=first_name, last_name=last_name, email=email)
            
            novcanik, _ = Novcanik.objects.get_or_create(korisnik=new_user)
            
            user_profile, created = UserProfile.objects.get_or_create(
                korisnik=new_user, 
                novcanik=novcanik, 
                defaults={
                    'ime': first_name,  
                    'prezime': last_name
                }
            )
            
            if not created:
                user_profile.ime = first_name
                user_profile.prezime = last_name
                user_profile.save()

            messages.success(request, 'Uspješno ste se registrirali. Sada se možete prijaviti.')
            return redirect('prijava')
        else:
            messages.error(request, 'Korisnik s ovim emailom već postoji.')

    return render(request, 'registracija.html')




def prijava(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Neuspješna prijava. Provjerite unesene podatke.')

    return render(request, 'prijava.html')

@login_required
def dashboard(request):
    korisnik = request.user
    user_profile = UserProfile.objects.get(korisnik=korisnik)
    korisnicki_balans = user_profile.novcanik.balance
    broj_aktivnih_preplata = UserSubscription.objects.filter(korisnik=korisnik, datum_isteka__gt=datetime.now()).count()

    datum_sada = datetime.now()
    pet_dana_od_sada = datum_sada + timedelta(days=5)
    uskoro_istice = UserSubscription.objects.filter(korisnik=korisnik, datum_isteka__range=(datum_sada, pet_dana_od_sada)).order_by('datum_isteka')

    current_time = timezone.now()
    announcements = Announcement.objects.filter(
        start_date__lte=current_time,
        end_date__gte=current_time,
        is_active=True
    )

    try:
        user_subscription = UserSubscription.objects.filter(korisnik=korisnik).latest('datum_pocetka')
        display_mag = all([user_subscription.mag_model, user_subscription.mag_mac, user_subscription.mag_sn])
    except UserSubscription.DoesNotExist:
        user_subscription = None
        display_mag = False

    context = {
        'korisnicki_balans': korisnicki_balans,
        'broj_aktivnih_preplata': broj_aktivnih_preplata,
        'uskoro_istice': uskoro_istice,
        'user_profile': user_profile,
        'announcements': announcements,
        'user_subscription': user_subscription,
        'display_mag': display_mag
    }

    return render(request, 'dashboard.html', context)


def prikaz_pretplata(request):
    pretplate = Subscription.objects.all()
    return render(request, 'prikaz_pretplata.html', {'pretplate': pretplate})

@login_required
def placanje_pretplate(request, pretplata_id):
    pretplata = Subscription.objects.get(id=pretplata_id)
    korisnik = request.user
    user_profile = UserProfile.objects.get(korisnik=korisnik)

    if request.method == 'POST':
        if user_profile.novcanik.oduzmi_sredstva(pretplata.cijena):
            UserSubscription.objects.create(korisnik=korisnik, pretplata=pretplata)
            return redirect('dashboard')  # Uspješno plaćanje, preusmjeri na dashboard
        else:
            poruka = "Nemate dovoljno sredstava za plaćanje ove pretplate."
            return render(request, 'placanje_pretplate.html', {'pretplata': pretplata, 'poruka': poruka})

    return render(request, 'placanje_pretplate.html', {'pretplata': pretplata})

@login_required
def lista_preplata(request):
    user = request.user  # Dohvat trenutno prijavljenog korisnika
    subscriptions = UserSubscription.objects.filter(korisnik=user)
    
    # Ažuriranje statusa isteklih pretplata
    now = datetime.now()
    expired_subscriptions = subscriptions.filter(datum_isteka__lte=now, status='P')
    for subscription in expired_subscriptions:
        subscription.status = 'I'
        subscription.save()
    
    # Obrni redoslijed pretplata tako da najnovija bude na vrhu
    reversed_subscriptions = reversed(subscriptions)
    
    context = {'subscriptions': reversed_subscriptions}
    return render(request, 'lista_preplata.html', context)

@login_required
def lista_kanala(request):
    kategorije = KategorijaKanala.objects.all()
    return render(request, 'lista_kanala.html', {'kategorije': kategorije})


@login_required
def balance(request):
    korisnik = request.user
    user_profile = UserProfile.objects.get(korisnik=korisnik)

    # Provjerite postoje li podaci o korisniku te dodajte ih u kontekst ako postoje
    ime = user_profile.ime if user_profile.ime else None
    prezime = user_profile.prezime if user_profile.prezime else None
    telefon = user_profile.broj_mobitela if user_profile.broj_mobitela else None
    balance = user_profile.novcanik.balance if user_profile.novcanik else None

    return render(request, 'balance.html', {'user_profile': user_profile, 'ime': ime, 'prezime': prezime, 'telefon': telefon, 'balance': balance})


@login_required
def podrska(request):
    return render(request, 'podrska.html')

@user_passes_test(is_admin)
def promijeni_status_preplate(request, user_subscription_id, new_status):
    try:
        user_subscription = UserSubscription.objects.get(id=user_subscription_id)
        user_subscription.status = new_status
        if new_status == 'P':
            user_subscription.datum_placanja = datetime.now()
            user_subscription.datum_pocetka = user_subscription.datum_placanja
            user_subscription.datum_isteka = user_subscription.datum_pocetka + timedelta(days=user_subscription.pretplata.trajanje_u_danima)
        user_subscription.save()
    except UserSubscription.DoesNotExist:
        pass

    return redirect('lista_preplata')


@login_required
def kupi_pretplatu(request):
    korisnik = request.user
    user_profile = UserProfile.objects.get(korisnik=korisnik)
    korisnicki_balans = user_profile.novcanik.balance
    datum_sada = datetime.now()
    pet_dana_od_sada = datum_sada + timedelta(days=5)
    uskoro_istice = UserSubscription.objects.filter(
        korisnik=korisnik, datum_isteka__range=(datum_sada, pet_dana_od_sada)).order_by('datum_isteka')
    zadnje_preplate = UserSubscription.objects.filter(
        korisnik=korisnik).order_by('-datum_pocetka')[:3]

    if request.method == 'POST':
        pretplata_id = request.POST.get('pretplata')

        try:
            pretplata = Subscription.objects.get(id=pretplata_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Pretplata ne postoji.')
            return render(request, 'kupi_pretplatu.html', {
                'pretplate': Subscription.objects.all(),
                'korisnicki_balans': korisnicki_balans,
                'uskoro_istice': uskoro_istice,
                'zadnje_preplate': zadnje_preplate,
                'TIP_USLUGE_CHOICES': UserProfile.TIP_USLUGE_CHOICES
            })

        mag_model = request.POST.get('mag_model', '')
        mag_mac = request.POST.get('mag_mac', '')
        mag_sn = request.POST.get('mag_sn', '')

        if mag_model and mag_mac and mag_sn:
            tip_usluge = 'MAG'
        else:
            tip_usluge = 'M3U'

        # Ažuriranje tip_usluge u UserProfile
        user_profile.tip_usluge = tip_usluge
        user_profile.save()

        if user_profile.novcanik.oduzmi_sredstva(pretplata.cijena):
            user_subscription = UserSubscription.objects.filter(
                korisnik=korisnik, pretplata=pretplata).first()

            if user_subscription and user_subscription in uskoro_istice:
                user_subscription.datum_isteka += timedelta(days=pretplata.trajanje_u_danima)
                user_subscription.save()
                messages.success(request, 'Uspješno ste produžili pretplatu!')
                # Pretpostavka: send_renewal_email funkcija već postoji
                send_renewal_email(user_profile, user_subscription)
                user_subscription.oznaci_nije_obavjesten()
            else:
                new_subscription = UserSubscription.objects.create(
                    korisnik=korisnik,
                    pretplata=pretplata,
                    datum_pocetka=datum_sada,
                    datum_isteka=datum_sada + timedelta(days=pretplata.trajanje_u_danima),
                    status='P',
                    mag_model=mag_model,
                    mag_mac=mag_mac,
                    mag_sn=mag_sn
                )
                messages.success(request, 'Uspješno ste kupili pretplatu!')
                new_subscription.admin_obavjesten_o_isteku = False
                new_subscription.korisnik_obavjesten_o_prekidu_usluge = False
                new_subscription.save()

                # Odabir e-mail predloška
                if tip_usluge == 'MAG':
                    email_template = 'korisnik_kupio_mag_preplatu_email.html'
                else:
                    email_template = 'korisnik_kupio_preplatu_email.html'

                context = {
                    'korisnik': korisnik,
                    'pretplata': pretplata,
                    'datum_pocetka': datum_sada.strftime('%d. %m. %Y'),
                    'datum_isteka': (datum_sada + timedelta(days=pretplata.trajanje_u_danima)).strftime('%d. %m. %Y'),
                    'mag_model': mag_model,
                    'mag_mac': mag_mac,
                    'mag_sn': mag_sn,
                    'm3u_link': user_profile.m3u_link if tip_usluge == 'M3U' else None,
                    'm3u_username': user_profile.m3u_username if tip_usluge == 'M3U' else None,
                    'm3u_password': user_profile.m3u_password if tip_usluge == 'M3U' else None
                }

                message_html = render_to_string(email_template, context)

                try:
                    send_mail(
                        "Nova uplata preplate", 
                        '', 
                        settings.EMAIL_HOST_USER, 
                        [settings.ADMIN_EMAIL], 
                        fail_silently=False, 
                        html_message=message_html
                    )
                    messages.success(request, 'E-mail je poslan.')
                except Exception as e:
                    messages.warning(request, f'E-mail nije poslan. Greška: {e}')

        else:
            messages.error(request, 'Nemate dovoljno sredstava za kupnju ove pretplate.')

    return render(request, 'kupi_pretplatu.html', {
        'pretplate': Subscription.objects.all(),
        'korisnicki_balans': korisnicki_balans,
        'uskoro_istice': uskoro_istice,
        'zadnje_preplate': zadnje_preplate,
        'TIP_USLUGE_CHOICES': UserProfile.TIP_USLUGE_CHOICES
    })



@login_required
def produzi_pretplatu(request, pretplata_id):
    korisnik = request.user
    active_subscriptions = UserSubscription.objects.filter(korisnik=korisnik, datum_isteka__gt=timezone.now())
    
    if not active_subscriptions.exists():
        return redirect('kupi_pretplatu')

    pretplata = Subscription.objects.get(id=pretplata_id)
    user_subscriptions = UserSubscription.objects.filter(korisnik=korisnik, pretplata=pretplata).order_by('-datum_isteka')

    if user_subscriptions.exists():
        user_subscription = user_subscriptions.first()
        user_profile = UserProfile.objects.get(korisnik=korisnik)

        if user_profile.novcanik.oduzmi_sredstva(pretplata.cijena):
            if user_subscription.datum_isteka < timezone.now():
                user_subscription.datum_isteka = timezone.now() + timedelta(days=pretplata.trajanje_u_danima)
            else:
                user_subscription.datum_isteka += timedelta(days=pretplata.trajanje_u_danima)

            user_subscription.save()

            messages.success(request, 'Uspješno ste produžili pretplatu!')
            send_renewal_email(user_profile, user_subscription)
            send_thank_you_email(user_profile, pretplata, user_subscription)
            user_subscription.oznaci_nije_obavjesten()
            user_subscription.admin_obavjesten_o_isteku = False
            user_subscription.korisnik_obavjesten_o_prekidu_usluge = False
            user_subscription.save()
        else:
            messages.error(request, 'Nemate dovoljno sredstava za produženje ove pretplate. Nadoplatite svoj račun kako biste nastavili.')
    else:
        messages.error(request, 'Nema odgovarajuće pretplate za produženje.')

    return redirect('kupi_pretplatu')




def send_admin_email(user_profile, pretplata, user_subscription, additional_info):
    subject = "Nova uplata preplate"
    context = {
        'korisnik': user_profile.korisnik,
        'pretplata': pretplata,
        'datum_pocetka': user_subscription.datum_pocetka.strftime('%d. %m. %Y'),
        'datum_isteka': user_subscription.datum_isteka.strftime('%d. %m. %Y'),
        'm3u_link': user_profile.m3u_link, 
        'm3u_username': user_profile.m3u_username,  
        'm3u_password': user_profile.m3u_password,
        'mag_model_uredjaja': additional_info.get('mag_model_uredjaja'),
        'mag_mac_adresa': additional_info.get('mag_mac_adresa'),
        'mag_sn': additional_info.get('mag_sn')
    }
    message_html = render_to_string('korisnik_kupio_mag_preplatu_email.html', context)
    send_mail(subject, '', settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL], fail_silently=False, html_message=message_html)



@login_required
def produzi_pretplatu_view(request, pretplata_id):
    korisnik = request.user
    pretplata = Subscription.objects.get(id=pretplata_id)
    user_subscription = UserSubscription.objects.get(korisnik=korisnik, pretplata=pretplata)

    produzi_pretplatu(user_subscription, pretplata)

    messages.success(request, 'Uspješno ste produžili pretplatu!')
    return redirect('lista_preplata')

@login_required
def kontakt_forma(request):
    message_sent = False  # Ova varijabla će biti True ako je poruka uspješno poslana
    if request.method == 'POST':
        ime = request.POST.get('ime')
        prezime = request.POST.get('prezime')
        email = request.POST.get('email')
        telefon = request.POST.get('telefon')
        naslov = request.POST.get('naslov')
        poruka = request.POST.get('poruka')

        # Spremanje poruke u bazu
        KontaktPoruka.objects.create(
            ime=ime,
            prezime=prezime,
            email=email,
            telefon=telefon,
            naslov=naslov,
            poruka=poruka
        )

        # Slanje HTML e-maila
        context = {
            'ime': ime,
            'prezime': prezime,
            'email': email,
            'telefon': telefon,
            'naslov': naslov,
            'poruka': poruka,
        }
        
        subject = naslov
        template_name = 'kontakt_form_email.html'  # Ime vašeg HTML predloška
        recipient_list = [settings.ADMIN_EMAIL]  # koristi postavke iz settings.py
        
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            html_message=html_message,
        )

        # Postavljanje varijable na True
        message_sent = True

    context = {'message_sent': message_sent, 'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY}
    return render(request, 'podrska.html', context)

def update_expired_subscriptions():
    expired_subscriptions = UserSubscription.objects.filter(datum_isteka__lte=datetime.now(), status='P')
    
    for subscription in expired_subscriptions:
        subscription.status = 'I'
        subscription.save()


# Obavjesti admina o produzivanju usluge 

def send_renewal_email(user_profile, user_subscription):
    # Osnovni kontekst za e-mail predložak
    email_context = {
        'ime': user_profile.ime,
        'prezime': user_profile.prezime,
        'email': user_profile.korisnik.email,
        'pretplata': user_subscription.pretplata.naziv,
        'cijena': user_subscription.pretplata.cijena,
        'datum_placanja': timezone.now().strftime('%d.%m.%Y'),
        'datum_isteka': user_subscription.datum_isteka.strftime('%d.%m.%Y'),
    }

    # Odabir HTML predloška i dodatnih informacija na temelju tipa usluge
    if user_profile.tip_usluge == 'MAG':
        html_template = 'korisnik_produzio_MAG_preplatu.html'
        email_context.update({
            'mag_model_uredjaja': user_subscription.mag_model,
            'mag_mac_adresa': user_subscription.mag_mac,
            'mag_sn': user_subscription.mag_sn,
        })
    else:  # Pretpostavimo da je tip usluge 'M3U' ako nije 'MAG'
        html_template = 'korisnik_produzio_preplatu.html'
        email_context.update({
            'm3u_link': user_profile.m3u_link,
            'm3u_username': user_profile.m3u_username,
            'm3u_password': user_profile.m3u_password,
        })

    # Učitajte HTML predložak za e-mail i proslijedite kontekst
    html_content = render_to_string(html_template, email_context)

    # Pošaljite e-mail
    send_mail(
        'Pretplata produžena',
        'Korisnik je produžio pretplatu.',
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
        html_message=html_content
    )


    # Funkcija za slanje zahvalnog e-maila korisniku
def send_thank_you_email(user_profile, pretplata, user_subscription):
    # Kontekst za e-mail predložak
    email_context = {
        'ime': user_profile.ime,
        'prezime': user_profile.prezime,
        'email': user_profile.korisnik.email,
        'pretplata': pretplata.naziv,
        'cijena': pretplata.cijena,
        'datum_placanja': timezone.now().strftime('%d.%m.%Y'),
        'datum_isteka': user_subscription.datum_isteka.strftime('%d.%m.%Y')
    }

    # Učitajte HTML predložak za e-mail i proslijedite kontekst
    html_content = render_to_string('zahvala_produzio_preplatu.html', email_context)

    # Pošaljite e-mail korisniku
    send_mail(
        'Vaša preplate je produžena',
        'Hvala što ste produžili svoju pretplatu.',
        settings.EMAIL_HOST_USER,
        [user_profile.korisnik.email],  # Korisnikova e-mail adresa
        fail_silently=False,
        html_message=html_content
    )


# Postavke
@login_required
def postavke(request):
    user_profile = request.user.userprofile  # Pretpostavljamo da je ovo već postavljeno u vašem kodu

    if request.method == 'POST':
        # Ažuriranje profila
        user_profile.ime = request.POST.get('ime', user_profile.ime)
        user_profile.prezime = request.POST.get('prezime', user_profile.prezime)
        request.user.email = request.POST.get('email', request.user.email)  # Ovdje je izmijenjeno
        user_profile.broj_mobitela = request.POST.get('telefon', user_profile.broj_mobitela)
        user_profile.drzava = request.POST.get('drzava', user_profile.drzava)

        if 'change_password' in request.POST:
            old_password = request.POST['old_password']
            new_password1 = request.POST['new_password1']
            new_password2 = request.POST['new_password2']

            if old_password and new_password1 and new_password2:
                if request.user.check_password(old_password):
                    if new_password1 == new_password2:
                        request.user.set_password(new_password1)
                        update_session_auth_hash(request, request.user)  # Osvježite sesiju da biste zadržali korisnika prijavljenim
                        messages.success(request, 'Vaša lozinka je uspješno promijenjena.')

                        # Trenutačni datum i vrijeme
                        now = datetime.now()
                        datum_promjene = now.strftime("%d.%m.%y")
                        vrijeme_promjene = now.strftime("%H:%M")

                        # Kontekst za e-mail predložak
                        email_context = {
                            'ime': user_profile.ime,
                            'datum_promjene': datum_promjene,
                            'vrijeme_promjene': vrijeme_promjene
                        }

                        # Učitajte HTML predložak za e-mail i proslijedite kontekst
                        html_content = render_to_string('lozinka_promjenjenja.html', email_context)

                        # Pošaljite e-mail
                        send_mail(
                            'Promjena lozinke',
                            'Vaša lozinka je uspješno promijenjena.',
                            settings.EMAIL_HOST_USER,  # Ovdje je dodano
                            [request.user.email],  # Ovdje je izmijenjeno
                            fail_silently=False,
                            html_message=html_content
                        )
                    else:
                        messages.error(request, 'Nova lozinka se ne podudara s potvrdom.')
                else:
                    messages.error(request, 'Stara lozinka nije ispravna.')

        # Ažuriranje modela korisnika i profila
        request.user.first_name = user_profile.ime  # Ovdje je izmijenjeno
        request.user.last_name = user_profile.prezime  # Ovdje je izmijenjeno
        request.user.save()  # Ovdje je izmijenjeno
        user_profile.save()
        messages.success(request, 'Vaš profil je uspješno ažuriran.')

    return render(request, 'postavke.html', {'user_profile': user_profile})




def obavijesti_korisnika_o_isteku(preplata):
    subject = 'Vaša pretplata uskoro ističe'
    context = {'pretplata': preplata}
    
    # Dobivanje samo imena korisnika
    ime_korisnika = preplata.korisnik.first_name
    
    context['ime_korisnika'] = ime_korisnika
    
    # Dodajte datum isteka u kontekst
    context['datum_isteka'] = preplata.datum_isteka.strftime('%d. %m. %Y')
    
    html_message = render_to_string('obavijest_o_isteku.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [preplata.korisnik.email]

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
    )
# HTML Mail


def send_html_email(subject, template_name, context, recipient_list):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.ADMIN_EMAIL,  # Koristite ADMIN_EMAIL iz settings.py za adresu pošiljatelja
        recipient_list,
        html_message=html_message,
    )

def send_email_view(request):
    # Kontekst za predložak e-pošte
    context = {
        'username': 'John Doe',
        'message': 'Dobrodošli u našu aplikaciju!',
    }
    
    # Popis primatelja e-pošte
    recipient_list = ['recipient1@example.com', 'recipient2@example.com']
    
    # Slanje HTML e-pošte
    send_html_email(
        subject='Dobrodošli!',
        template_name='email',  # Ime vašeg HTML predloška
        context=context,
        recipient_list=recipient_list,
    )
    
    return render(request, 'email_sent.html')

# PayPal 

def paypal_payment(request):
    PAYPAL_CLIENT_ID = getattr(settings, "PAYPAL_CLIENT_ID", None)
    PAYPAL_SECRET_KEY = getattr(settings, "PAYPAL_SECRET_KEY", None)

    if PAYPAL_CLIENT_ID is None or PAYPAL_SECRET_KEY is None:
        return JsonResponse({'status': 'error', 'error': 'PayPal settings are not configured.'})
    
    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_SECRET_KEY
    })

    if request.method == 'POST':
        amount = request.POST.get('amount', '0.0')
        return_url = request.build_absolute_uri(reverse('paypal_return'))  # Generisanje return_url
        cancel_url = request.build_absolute_uri(reverse('paypal_cancel'))  # Generisanje cancel_url
        
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Nadopuna novčanika",
                        "sku": "sku",
                        "price": amount,
                        "currency": "EUR",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": amount,
                    "currency": "EUR"
                },
                "description": "Nadopuna vašeg novčanika."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
            return JsonResponse({'status': 'success', 'paymentID': payment.id, 'approval_url': approval_url})
        else:
            return JsonResponse({'status': 'error', 'error': str(payment.error)})

    return JsonResponse({'status': 'error', 'error': 'Invalid request'})

# Slanje maila korsitniku da je uspesno nadoplatio svoj racun 

def send_payment_confirmation_email(user_email, amount):
    user_profile = UserProfile.objects.get(korisnik__email=user_email)
    balance_before = user_profile.novcanik.balance  # Trenutni balans prije uplate
    new_balance = balance_before + Decimal(amount)  # Novi balans nakon uplate
    
    subject = 'Uspješno ste nadoplatili svoj novčanik'
    html_message = render_to_string('novcanik_nadoplacen.html', {
        'user': user_profile,
        'amount': amount,
        'balance_before': balance_before,
        'new_balance': new_balance,
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = user_email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)



@login_required
def paypal_return(request):
    print("Is user authenticated?", request.user.is_authenticated)
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    # Preuzmite Payment objekat koristeći PayPal SDK
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):  # Ovdje izvršite plaćanje
        # Ako je plaćanje uspešno, ažurirajte korisnikov novčanik
        korisnik = request.user
        user_profile = UserProfile.objects.get(korisnik=korisnik)
        amount = float(payment['transactions'][0]['amount']['total'])  # Pretpostavimo da je iznos spremljen u 'total'
        
        user_profile.novcanik.dodaj_sredstva(amount)
        send_payment_confirmation_email(user_profile.korisnik.email, amount)  # Pristupamo emailu putem ForeignKey-a
        
        # Dodajte poruku o uspješnoj nadoplati korisniku
        messages.success(request, f'Uspješno ste nadoplatili račun za {amount} €.')
        
        # Dodajte dodatne korake kao što je slanje obaveštenja putem e-maila, itd.
        
        return redirect('balance')
        
    else:
        # Neuspješno plaćanje, preusmjerite korisnika na odgovarajuću stranicu
        return redirect('dashboard')

@login_required
def paypal_cancel(request):
    # Opciono, dodajte poruku korisniku da je transakcija otkazana
    messages.add_message(request, messages.INFO, 'Transakcija je otkazana.')
    
    # Preusmerite korisnika na odgovarajuću stranicu
    return redirect('dashboard')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def provjera_preplata(request):
    provjeri_istek_preplata()
    return HttpResponse('Provjera obavljena', content_type='text/plain')


def update_m3u_status(request):
    if request.method == 'POST':
        user_profile_id = request.POST.get('user_profile_id')
        user_profile = UserProfile.objects.get(id=user_profile_id)
        user_profile.is_m3u_active = not user_profile.is_m3u_active
        user_profile.save()
    return redirect('dashboard')