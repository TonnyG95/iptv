from django.contrib import admin
from .models import Subscription, Novcanik, UserProfile, UserSubscription, KategorijaKanala, Kanal, KontaktPoruka, Announcement

# Kategorija Kanala
@admin.register(KategorijaKanala)
class KategorijaKanalaAdmin(admin.ModelAdmin):
    list_display = ['naziv']

# Kanali 
@admin.register(Kanal)
class KanalAdmin(admin.ModelAdmin):
    list_display = ['naziv', 'kategorija']

# Prilagođena administracija za model Subscription
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'cijena', 'trajanje_u_danima')

# Prilagođena administracija za model Novcanik
class NovcanikAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'balance')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'ime', 'prezime', 'drzava', 'broj_mobitela', 'm3u_username', 'm3u_password', 'is_m3u_active')  # Dodajte 'is_m3u_active' u list_display
    list_editable = ('is_m3u_active',)  # Dodajte 'is_m3u_active' u list_editable da omogućite promjenu statusa iz liste
    list_filter = ('is_m3u_active',)  # Dodajte 'is_m3u_active' u list_filter za filtriranje prema statusu


# Prilagođena administracija za model UserSubscription
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'pretplata', 'status', 'datum_pocetka', 'datum_isteka')
    list_filter = ('status',)

    actions = ['oznaci_placeno', 'oznaci_treba_platiti', 'oznaci_isteklo']

    def oznaci_placeno(self, request, queryset):
        queryset.update(status='P')
    oznaci_placeno.short_description = 'Označi odabrane preplate kao plaćene'

    def oznaci_treba_platiti(self, request, queryset):
        queryset.update(status='T')
    oznaci_treba_platiti.short_description = 'Označi odabrane preplate kao treba platiti'

    def oznaci_isteklo(self, request, queryset):
        queryset.update(status='I')
    oznaci_isteklo.short_description = 'Označi odabrane preplate kao istekle'

# Prilagođena administracija za model KontaktPoruka
@admin.register(KontaktPoruka)
class KontaktPorukaAdmin(admin.ModelAdmin):
    list_display = ('ime', 'prezime', 'email', 'telefon', 'naslov', 'poruka', 'datum_poslano')
    search_fields = ('ime', 'prezime', 'email', 'naslov')
    list_filter = ('datum_poslano', )
    ordering = ('-datum_poslano', )

# Registracija modela s prilagođenom administracijom
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Novcanik, NovcanikAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)

# Prilagođena administracija za model Announcement
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    ordering = ('-start_date',)
