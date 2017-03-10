from django.conf import settings as django_settings
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language

def settings(request):
    return {'settings': django_settings}



def alternate_seo_url(request):
    alternate_url = dict()
    path = request.path
    url_parts = resolve( path )
    url = path
    cur_language = get_language()
    for lang_code, lang_name in django_settings.LANGUAGES :
        try:
            activate(lang_code)
            url = reverse( url_parts.view_name, kwargs=url_parts.kwargs )
            alternate_url[lang_code] = django_settings.SITE_URL+url
        finally:
            activate(cur_language)

    return {'alternate':alternate_url}
