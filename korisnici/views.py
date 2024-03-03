from .models import UserProfile

def korisnicki_balans(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(korisnik=request.user)
        korisnicki_balans = user_profile.novcanik.balance
    else:
        korisnicki_balans = 0.0

    return {'korisnicki_balans': korisnicki_balans}
