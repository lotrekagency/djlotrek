from collections import OrderedDict
from django.conf import settings as django_settings
try:
    from django.core.urlresolvers import reverse, resolve
except ImportError:
    from django.urls import reverse, resolve
from django.utils.translation import activate, get_language
from urllib.parse import urljoin

from .request_utils import get_host_url


def group_queryset_by_attribute(queryset, attribute):
    grouped = dict()
    for obj in queryset:
        grouped.setdefault(getattr(obj, attribute), []).append(obj)
    return grouped


def group_objects_by_attribute(objects, attribute):
    return group_queryset_by_attribute(objects, attribute)


def order_dict_from_list(queue, key_order):
    new_queue = OrderedDict()
    for key in key_order:
        if key in queue:
            new_queue[key] = queue[key]
    return new_queue


def alternate_seo_url_with_object(request, obj_class, **kwargs):
    alternate_url = dict()
    path = request.path
    url_parts = resolve(path)
    base_url = get_host_url(request)
    cur_language = get_language()
    if not url_parts.app_names:
        main_obj = obj_class.objects.language().get(**kwargs)
        for lang_code, lang_name in django_settings.LANGUAGES:
            try:
                activate(lang_code)
                args = []
                obj = obj_class.objects.language().get(pk=main_obj.pk)
                for kwarg_key, kwarg_val in kwargs.items():
                    args.append(getattr(obj, kwarg_key))
                url = reverse(
                    url_parts.view_name,
                    args=args
                )
                alternate_url[lang_code] = urljoin(base_url, url)
            except obj_class.DoesNotExist:
                pass
    activate(cur_language)
    return alternate_url
