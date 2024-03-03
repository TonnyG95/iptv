from django.contrib import admin
from .models import PostavkePlatforme, Link, DrustveneMreze

class LinkInline(admin.TabularInline):
    model = PostavkePlatforme.linkovi.through
    extra = 1

class DrustveneMrezeInline(admin.TabularInline):
    model = PostavkePlatforme.drustvene_mreze.through
    extra = 1

class PostavkePlatformeAdmin(admin.ModelAdmin):
    list_display = ['ime_platforme']
    fieldsets = (
        ('Osnovne postavke', {
            'fields': ('ime_platforme', 'logo', 'white_logo', 'favicon', 'politika_privatnosti', 'uvijeti_koristenja')
        }),
        ('Društvene mreže', {
            'fields': ('facebook_link', 'instagram_link', 'whatsapp_link')
        }),
        ('Dashboard', {
            'fields': ('dashboard_pocetna_header', 'dashboard_pocetna_opis')
        }),
        ('Navigacija', {
            'fields': ('preplate_heading', 'lista_kanala_heading')
        }),
        ('Novčanik', {
            'fields': ('novcanik_heading', 'novcanik_informacije_heder', 'novcanik_napodplati_novcanik_header', 'novcanik_nadoplati_novcanik_opis')
        }),
        ('Podrška i Profil', {
            'fields': ('podrska_heading', 'postavke_profila_heading')
        }),
        ('Početna kartica', {
            'fields': ('pocetna_kartica_balans_card_header', 'pocetna_kartica_balans_opis', 'pocetna_kartica_aktivne_usluge_card_header', 'pocetna_kartica_aktivne_usluge_opis', 'pocetna_kartica_usluge_koje_isticu_card_header', 'pocetna_kartica_usluge_koje_isticu_opis')
        }),
        ('Email postavke', {
            'fields': ('email_opis', 'email_website_link', 'email_support_mail', 'email_support_phone')
        }),
    )
    inlines = [LinkInline, DrustveneMrezeInline]

admin.site.register(Link)
admin.site.register(DrustveneMreze)
admin.site.register(PostavkePlatforme, PostavkePlatformeAdmin)
