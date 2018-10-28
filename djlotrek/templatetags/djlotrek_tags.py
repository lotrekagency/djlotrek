import datetime
import re

from django import template
try:
    from django.core.urlresolvers import reverse, NoReverseMatch
except ImportError:
    from django.urls import reverse, NoReverseMatch

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
def active(context, pattern_or_urlname, **kwargs):
    try:
        pattern = '^' + reverse(pattern_or_urlname, kwargs=kwargs)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.simple_tag(takes_context=True)
def absolute_url(context, url):
    host = get_host_url('' if 'request' not in context else context['request'])
    if url:
        return urljoin(host, url)
    else:
        return ''
