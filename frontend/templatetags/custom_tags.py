from django import template
from frontend.models import PostavkePlatforme

register = template.Library()

@register.simple_tag
def get_platform_settings():
    return PostavkePlatforme.objects.first()
