from django import template
from django.core import urlresolvers


register = template.Library()


@register.simple_tag(takes_context=True)
def link_build(context, build):
    if build:
        return urlresolvers.reverse("admin:core_build_change", args=[build.id])
    return ''
