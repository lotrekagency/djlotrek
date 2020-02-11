from django.conf import settings as django_settings
try:
    from django.core.urlresolvers import reverse, resolve
except ImportError:
    from django.urls import reverse, resolve
from django.utils.translation import activate, get_language
from urllib.parse import urljoin

from .request_utils import get_host_url


def settings(request):
    return {'settings': django_settings}


def alternate_seo_url(request):
    try:
        alternate_url = dict()
        path = request.path
        url_parts = resolve(path)
        base_url = get_host_url(request)
        cur_language = get_language()
        if not url_parts.app_names:
            for lang_code, lang_name in django_settings.LANGUAGES:
                activate(lang_code)
                url = reverse(
                    url_parts.view_name,
                    kwargs=url_parts.kwargs
                )
                alternate_url[lang_code] = urljoin(base_url, url)
        activate(cur_language)
        return {'alternate_urls': alternate_url}
    except: # NOQA
        return {'alternate_urls': {}}
