from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from korisnici.models import UserProfile, Novcanik, UserSubscription
import logger

@receiver(post_delete, sender=User)
def obrisi_povezani_profil_i_novcanik(sender, instance, **kwargs):
    try:
        profil_korisnika = UserProfile.objects.get(korisnik=instance)
        profil_korisnika.delete()
    except UserProfile.DoesNotExist:
        pass
    
    try:
        novcanik = Novcanik.objects.get(korisnik=instance)
        novcanik.delete()
    except Novcanik.DoesNotExist:
        pass

