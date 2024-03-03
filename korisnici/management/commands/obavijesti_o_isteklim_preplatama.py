from django.core.management.base import BaseCommand
from django.utils import timezone
from korisnici.models import UserSubscription
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from frontend.views import obavijesti_korisnika_o_isteku


class Command(BaseCommand):
    help = 'Šalje obavijesti adminu o isteklim preplatama i korisnicima o preplatama koje će uskoro isteći'

    def handle(self, *args, **options):
        now = timezone.now()
        five_days_from_now = now + timedelta(days=5)
        five_days_ago = now - timedelta(days=5)

        expired_subscriptions = UserSubscription.objects.filter(datum_isteka__lte=now, status='P')
        expiring_subscriptions = UserSubscription.objects.filter(datum_isteka__range=(now, five_days_from_now), status='P')
        expired_five_days_ago_subscriptions = UserSubscription.objects.filter(datum_isteka__range=(five_days_ago, now), status='N')

        if expired_subscriptions.exists():
            message = "Istekle su sljedeće preplate:\n"
            for subscription in expired_subscriptions:
                message += f"{subscription.korisnik.username} - {subscription.pretplata.naziv}\n"

            # Generirajte HTML poruku iz predloška
            html_message = render_to_string('email.html', {'message': message})

            send_mail(
                "Istekle preplate",
                strip_tags(html_message),  # Tekstualna verzija HTML poruke
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )

        if expired_five_days_ago_subscriptions.exists():
            message = "Slijedećim korisnicima je pretplata istekla prije 5 dana:\n"
            for subscription in expired_five_days_ago_subscriptions:
                message += f"{subscription.korisnik.username} - {subscription.pretplata.naziv}\n"

            # Generirajte HTML poruku iz predloška
            html_message = render_to_string('email.html', {'message': message})

            send_mail(
                "Pretplate istekle prije 5 dana",
                strip_tags(html_message),  # Tekstualna verzija HTML poruke
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )

        if expiring_subscriptions.exists():
            admin_message = "Slijedeće preplate će uskoro isteći:\n"
            for subscription in expiring_subscriptions:
                admin_message += f"{subscription.korisnik.username} - {subscription.pretplata.naziv} (istječe {subscription.datum_isteka})\n"

            # Generirajte HTML poruku iz predloška
            admin_html_message = render_to_string('email.html', {'message': admin_message, 'subscription': subscription})

            # Slanje e-maila adminu s HTML porukom
            send_mail(
                "Usporočno istečuće preplate",
                strip_tags(admin_html_message),  # Tekstualna verzija HTML poruke
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                html_message=admin_html_message,
                fail_silently=False,
            )
            
            # Slanje e-maila korisnicima
            for subscription in expiring_subscriptions:
                obavijesti_korisnika_o_isteku(subscription)
