import re

from django import template
import datetime
from django.core.urlresolvers import reverse, NoReverseMatch

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
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
