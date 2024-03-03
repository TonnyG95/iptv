from .models import UserProfile

def global_user_profile(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(korisnik=request.user)
        return {'global_user_profile': user_profile}
    return {}
