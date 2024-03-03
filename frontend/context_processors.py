from frontend.models import PostavkePlatforme

def platform_settings(request):
    settings = PostavkePlatforme.objects.first()
    context = {}

    if settings:
        for field in PostavkePlatforme._meta.fields:
            context[field.name] = getattr(settings, field.name)

        context['linkovi'] = settings.linkovi.all()
        context['drustvene_mreze'] = settings.drustvene_mreze.all()
        context['white_logo'] = settings.white_logo.url if settings.white_logo else None

    return context
