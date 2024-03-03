from datetime import timedelta, datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from korisnici.models import UserSubscription
from django.core.management.base import BaseCommand
import logging

# Konfiguracija loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def obavijesti_korisnika_o_isteku(preplata):
    # Provjerite je li korisnik već obaviješten
    if not preplata.korisnik_obavjesten_o_isteku:
        subject = 'Vaša pretplata će uskoro isteći'
        context = {
            'ime': preplata.korisnik.first_name,
            'prezime': preplata.korisnik.last_name,
            'naziv_preplate': preplata.pretplata.naziv,
            'datum_isteka': preplata.datum_isteka
        }
        html_content = render_to_string('obavijest_o_isteku.html', context)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [preplata.korisnik.email]
        try:
            send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=html_content)
            logger.info(f"E-mail poslan korisniku {preplata.korisnik.email} o isteku pretplate.")
            
            # Postavite korisnik_obavjesten_o_isteku na True
            preplata.oznaci_obavjesten()
        except Exception as e:
            logger.error(f"Greška prilikom slanja e-pošte korisniku {preplata.korisnik.email}. Detalji greške: {e}")
    else:
        logger.info(f"Korisnik {preplata.korisnik.email} je već obaviješten o isteku pretplate.")



def obavijesti_admina_o_isteku(preplata):
    # Ako je admin već obaviješten, nema potrebe za slanjem e-maila opet
    if preplata.admin_obavjesten_o_isteku:
        return

    # Naslov e-maila
    subject = 'Obavijest o isteku pretplate'
    
    # Dohvaćanje profila korisnika
    user_profile = preplata.korisnik.userprofile
    
    # Osnovne informacije za e-mail
    email_context = {
        'ime': user_profile.ime,
        'prezime': user_profile.prezime,
        'email_korisnika': preplata.korisnik.email,
        'naziv_preplate': preplata.pretplata.naziv,
        'datum_isteka': preplata.datum_isteka,
    }
    
    # Odabir predloška i dodatne informacije temeljem tipa usluge
    if user_profile.tip_usluge == 'MAG':
        html_template = 'admin_obavijest_MAG_istek.html'
        email_context.update({
            'mag_model_uredjaja': preplata.mag_model,
            'mag_mac_adresa': preplata.mag_mac,
            'mag_sn': preplata.mag_sn,
        })
    else:
        html_template = 'korisniku_usluga_ugasena.html'
        email_context.update({
            'm3u_link': user_profile.m3u_link,
            'm3u_username': user_profile.m3u_username,
            'm3u_password': user_profile.m3u_password,
        })
    
    # Kreiranje HTML sadržaja e-maila
    html_content = render_to_string(html_template, email_context)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.ADMIN_EMAIL]
    
    try:
        # Slanje e-maila
        send_mail(subject, '', from_email, recipient_list, html_message=html_content)
        logger.info(f"E-mail poslan adminu o isteku pretplate korisnika {preplata.korisnik.email}.")
        
        # Postavljanje statusa da je admin obaviješten
        preplata.admin_obavjesten_o_isteku = True
        preplata.save()

    except Exception as e:
        logger.error(f"Greška prilikom slanja e-pošte adminu o isteku pretplate korisnika {preplata.korisnik.email}. Detalji greške: {e}")




def obavijesti_korisnika_o_ukidanju_usluge(preplata):
    if not preplata.korisnik_obavjesten_o_prekidu_usluge:
        subject = 'Vaša pretplata je istekla'
        context = {
            'ime': preplata.korisnik.first_name,
            'prezime': preplata.korisnik.last_name,
            'naziv_preplate': preplata.pretplata.naziv,
            'datum_isteka': preplata.datum_isteka
        }
        html_content = render_to_string('korisniku_preplata_istekla.html', context)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [preplata.korisnik.email]
        try:
            send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=html_content)
            logger.info(f"E-mail poslan korisniku {preplata.korisnik.email} o ukinutoj usluzi.")
            
            # Ažuriranje statusa nakon što je e-mail uspješno poslan
            preplata.korisnik_obavjesten_o_prekidu_usluge = True
            preplata.save()
            
        except Exception as e:
            logger.error(f"Greška prilikom slanja e-pošte korisniku {preplata.korisnik.email} o ukinutoj usluzi. Detalji greške: {e}")
    else:
        logger.info(f"Korisnik {preplata.korisnik.email} već je obaviješten o ukinutoj usluzi.")


def provjeri_istek_preplata():
    now = timezone.now()
    logger.info(f"Trenutačno vrijeme: {now}")

    # Pretplate koje će isteći za 5 dana
    pet_dana_od_sada = now + timedelta(days=5)
    logger.info(f"Tražimo pretplate koje će isteći unutar sljedećih 5 dana, do datuma: {pet_dana_od_sada}")

    upcoming_expirations = UserSubscription.objects.filter(datum_isteka__date=pet_dana_od_sada.date(), status='P')
    for preplata in upcoming_expirations:
        obavijesti_korisnika_o_isteku(preplata)

    # Pretplate koje su istekle prije 5 dana
    five_days_ago = now - timedelta(days=5)
    logger.info(f"Tražimo pretplate koje su istekle prije 5 dana, odnosno na datum: {five_days_ago}")

    expired_five_days_ago = UserSubscription.objects.filter(datum_isteka__date=five_days_ago.date(), status='E')
    for subscription in expired_five_days_ago:
        logger.info(f"Pretplata koja je istekla na datum: {subscription.datum_isteka}")
        obavijesti_admina_o_isteku(subscription)
        obavijesti_korisnika_o_ukidanju_usluge(subscription)
        # Ovdje ne morate postavljati status jer će vaš model automatski postaviti status na 'E' kada datum isteka prođe


class Command(BaseCommand):
    help = 'Dnevna provjera preplata i obavještavanje korisnika'

    def handle(self, *args, **kwargs):
        provjeri_istek_preplata()