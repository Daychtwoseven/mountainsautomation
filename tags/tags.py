from django import template
from app.models import *


register = template.Library()


@register.simple_tag
def urls():
    return Urls.objects.filter(is_active=True).order_by('id')