from django.db import models

class Link(models.Model):
    ime_linka = models.CharField(max_length=100)
    link_url = models.URLField()

    def __str__(self):
        return self.ime_linka
    
class DrustveneMreze(models.Model):  # Promijenjeno ime klase
    ime_mreze = models.CharField(max_length=100)  # Promijenjeno ime polja
    link_mreze = models.URLField()  # Promijenjeno ime polja
    ikona_mreze = models.ImageField(upload_to='ikone_mreza/', blank=True, null=True)  # Promijenjeno ime polja i putanja

    def __str__(self):
        return self.ime_mreze  # Promijenjeno ime polja

class PostavkePlatforme(models.Model):
    ime_platforme = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    politika_privatnosti = models.URLField(blank=True, null=True)
    uvijeti_koristenja = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    dashboard_pocetna_header = models.CharField(max_length=200, blank=True, null=True)
    dashboard_pocetna_opis = models.TextField(blank=True, null=True)
    preplate_heading = models.CharField(max_length=100, blank=True, null=True)
    lista_kanala_heading = models.CharField(max_length=100, blank=True, null=True)
    novcanik_heading = models.CharField(max_length=100, blank=True, null=True)
    podrska_heading = models.CharField(max_length=100, blank=True, null=True)
    postavke_profila_heading = models.CharField(max_length=100, blank=True, null=True)
    pocetna_kartica_balans_card_header = models.CharField(max_length=100, blank=True, null=True)
    pocetna_kartica_balans_opis = models.TextField(blank=True, null=True)
    pocetna_kartica_aktivne_usluge_card_header = models.CharField(max_length=100, blank=True, null=True)
    pocetna_kartica_aktivne_usluge_opis = models.TextField(blank=True, null=True)
    pocetna_kartica_usluge_koje_isticu_card_header = models.CharField(max_length=100, blank=True, null=True)
    pocetna_kartica_usluge_koje_isticu_opis = models.TextField(blank=True, null=True)
    novcanik_informacije_heder = models.CharField(max_length=100, blank=True, null=True)
    novcanik_napodplati_novcanik_header = models.CharField(max_length=100, blank=True, null=True)
    novcanik_nadoplati_novcanik_opis = models.TextField(blank=True, null=True)
    email_opis = models.TextField(blank=True, null=True)
    email_website_link = models.TextField(blank=True, null=True)
    email_support_mail = models.TextField(blank=True, null=True)
    email_support_phone = models.TextField(blank=True, null=True)
    linkovi = models.ManyToManyField(Link, blank=True)
    drustvene_mreze = models.ManyToManyField(DrustveneMreze, blank=True)  # Promijenjeno ime klase i polja
    white_logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.ime_platforme
