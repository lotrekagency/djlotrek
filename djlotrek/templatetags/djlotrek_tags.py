import datetime

from django import template
try:
    from django.core.urlresolvers import resolve
except ImportError:
    from django.urls import resolve

from djlotrek import get_host_url
from urllib.parse import urljoin


register = template.Library()


@register.simple_tag
def auto_update_year_range(start=None):
    current_year = datetime.datetime.now().year
    if start == current_year:
        return current_year
    if start:
        return '{0}-{1}'.format(start, current_year)
    return current_year


@register.simple_tag(takes_context=True)
def active(context, url_name):
    request = context['request']
    try:
        if url_name == resolve(request.path_info).url_name:
            return 'active'
    except: # NOQA
        pass
    return ''


@register.simple_tag(takes_context=True)
def absolute_url(context, url):
    host = get_host_url('' if 'request' not in context else context['request'])
    if url:
        return urljoin(host, url)
    else:
        return ''
