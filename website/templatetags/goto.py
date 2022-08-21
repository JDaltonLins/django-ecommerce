from django import template
from urllib.parse import urlencode
from django.urls import reverse

register = template.Library()


@register.simple_tag
def goto(*_, **kwargs):
    rever = reverse(_[0])
    return rever + '?' + urlencode(kwargs)
