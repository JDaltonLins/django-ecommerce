from django import template
from urllib.parse import urlencode
from django.template import RequestContext

register = template.Library()


@register.simple_tag(takes_context=True)
def redirect(context: RequestContext, *_, **kwargs):
    props = context.request.GET.dict()

    for k, v in kwargs.items():
        if v is None and k in props:
            props.pop(k)
        elif v is not None:
            props[k] = v

    return context.request.path + '?' + urlencode(props)
