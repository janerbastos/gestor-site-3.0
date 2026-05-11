from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from a_Site.services import MediaStorageService


register = template.Library()


@register.simple_tag
def media_storage_card():

    storage = MediaStorageService.get_storage_info()

    html = render_to_string(
        'site/components/storage/storage_card.html',
        {
            'storage': storage
        }
    )

    return mark_safe(html)