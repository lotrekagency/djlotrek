from django import template
import datetime


register = template.Library()


@register.simple_tag
def auto_update_year_range(start=None):
    current_year = datetime.datetime.now().year
    if start == current_year:
        return current_year
    if start:
        return '{0}-{1}'.format(start, current_year)
    return current_year
