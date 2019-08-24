from django import template
import re

register = template.Library()


@register.filter(name='media_url')
def media_url(media):
    return getattr(media, 'url', '')


@register.filter(name='key')
def key(d, key_name):
    if key_name in d:
        return d[key_name]


@register.filter(name='is_in')
def is_in(value, args):
    return value in args.split(',')


@register.filter(name='is_not_in')
def is_not_in(value, args):
    return not is_in(value, args)


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter(name='get_sorted')
def get_sorted(value):
    return sorted(value)


@register.filter(name='regex_match')
def regex_match(value, regex):
    pattern = re.compile(regex, re.U | re.I)
    if pattern.match(value):
        return True
    return False
