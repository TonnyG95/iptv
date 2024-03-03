from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, datetime
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import pre_save
import string
import random


# Preplate

class Subscription(models.Model):
    naziv = models.CharField(max_length=100)
    cijena = models.DecimalField(max_digits=10, decimal_places=2)
    trajanje_u_danima = models.PositiveIntegerField()
    funkcije = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.naziv

# Novcanik

class Novcanik(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Novčanik korisnika {self.korisnik.username}"

    def oduzmi_sredstva(self, iznos):
        if self.balance >= iznos:
            self.balance -= iznos
            self.save()
            return True
        return False

    def dodaj_sredstva(self, iznos):
        self.balance += Decimal(iznos)
        self.save()

# Profili

class UserProfile(models.Model):
    TIP_USLUGE_CHOICES = [
        ('M3U', 'M3U'),
        ('MAG', 'MAG'),
    ]

    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    ime = models.CharField(max_length=100)
    prezime = models.CharField(max_length=100)
    drzava = models.CharField(max_length=100)
    broj_mobitela = models.CharField(max_length=20)
    novcanik = models.OneToOneField(Novcanik, on_delete=models.CASCADE)
    m3u_username = models.CharField(max_length=100, blank=True, null=True)
    m3u_password = models.CharField(max_length=100, blank=True, null=True)
    m3u_link = models.TextField(blank=True, null=True)
    is_m3u_active = models.BooleanField(default=False)
    tip_usluge = models.CharField(max_length=4, choices=TIP_USLUGE_CHOICES, null=True, blank=True)
    mag_model = models.CharField(max_length=100, default='', blank=True)
    mag_mac = models.CharField(max_length=100, default='', blank=True)
    mag_sn = models.CharField(max_length=100, default='', blank=True)

    def replace_special_characters(self, text):
        replace_dict = {
            'š': 's', 'đ': 'dj', 'ž': 'z', 'ć': 'c', 'č': 'c',
            'Š': 'S', 'Đ': 'Dj', 'Ž': 'Z', 'Ć': 'C', 'Č': 'C'
        }
        for k, v in replace_dict.items():
            text = text.replace(k, v)
        return text

    def generate_m3u_username(self):
        ime_cap = self.replace_special_characters(self.ime.capitalize())
        prezime_cap = self.replace_special_characters(self.prezime.capitalize())
        return f"{ime_cap}{prezime_cap}IPTV"

    def generate_m3u_password(self, length=10):
        characters = string.ascii_letters + string.digits  # mala slova, velika slova, brojevi
        password = ''.join(random.choice(characters) for i in range(length))
        return self.replace_special_characters(password)

    def generate_m3u_link(self):
        base_url = "http://ott.global-telecom.eu:25461/get.php?"
        return f"{base_url}username={self.m3u_username}&password={self.m3u_password}&type=m3u_plus&output=mpegts"

    def save(self, *args, **kwargs):
        # Ovdje postavljamo m3u_username, m3u_password, i m3u_link prije nego što se objekt spremi
        if not self.m3u_username and self.ime and self.prezime:
            self.m3u_username = self.generate_m3u_username()
        if not self.m3u_password:
            self.m3u_password = self.generate_m3u_password()
        if not self.m3u_link and self.m3u_username and self.m3u_password:
            self.m3u_link = self.generate_m3u_link()
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.korisnik.username

        

# Aktivne preplate

class UserSubscription(models.Model):
    STATUS_CHOICES = (
        ('P', 'Plaćena'),
        ('N', 'Treba platiti'),
        ('E', 'Istekla'),
    )

    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    pretplata = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    datum_pocetka = models.DateTimeField(null=True, blank=True)
    datum_isteka = models.DateTimeField()
    datum_placanja = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    mag_model = models.CharField(max_length=100, default='', blank=True, null=True)
    mag_mac = models.CharField(max_length=100, default='', blank=True, null=True)
    mag_sn = models.CharField(max_length=100, default='', blank=True, null=True)
    is_mag_active = models.BooleanField(default=False)
    korisnik_obavjesten_o_isteku = models.BooleanField(default=False)
    admin_obavjesten_o_isteku = models.BooleanField(default=False)
    korisnik_obavjesten_o_prekidu_usluge = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.datum_isteka = timezone.now() + timezone.timedelta(days=self.pretplata.trajanje_u_danima)
        
        if self.datum_isteka < timezone.now():
            self.status = 'E'
        elif self.status != 'P':
            self.status = 'N'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pretplata {self.pretplata.naziv} za korisnika {self.korisnik.username}"
    
    def oznaci_obavjesten(self):
        self.korisnik_obavjesten_o_isteku = True
        self.save()

    def oznaci_nije_obavjesten(self):
        self.korisnik_obavjesten_o_isteku = False
        self.save()




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        novcanik = Novcanik.objects.create(korisnik=instance)
        UserProfile.objects.create(korisnik=instance, novcanik=novcanik)

# Lista Kanala

class KategorijaKanala(models.Model):
    naziv = models.CharField(max_length=100)

    def __str__(self):
        return self.naziv


class Kanal(models.Model):
    kategorija = models.ForeignKey(KategorijaKanala, on_delete=models.CASCADE)
    naziv = models.CharField(max_length=100)

    def __str__(self):
        return self.naziv

class KontaktPoruka(models.Model):
    ime = models.CharField(max_length=255)
    prezime = models.CharField(max_length=255)
    email = models.EmailField()
    telefon = models.CharField(max_length=20)
    naslov = models.CharField(max_length=255)
    poruka = models.TextField()
    datum_poslano = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ime} {self.prezime} - {self.naslov}"
    
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    start_date = models.DateTimeField(help_text="Datum kada će se obavijest početi prikazivati.")
    end_date = models.DateTimeField(help_text="Datum kada će obavijest prestati prikazivati.")
    is_active = models.BooleanField(default=True, help_text="Označite ako želite da se obavijest prikazuje ili ne prikazuje manualno.")
    
    def __str__(self):
        return self.title