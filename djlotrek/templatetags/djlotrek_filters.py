from django import template
import re

register = template.Library()


@register.filter(name='label')
def label(queryset, args):
    identifier, attr = args.split(',')
    filtered_objects = queryset.filter(identifier=identifier)
    if len(filtered_objects):
        return getattr(filtered_objects[0], attr)
    return ''


@register.filter(name='media_url')
def media_url(media):
    if media:
        return media.url
    return ''


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
    pattern = re.compile(regex)
    if pattern.match(value):
        return True
