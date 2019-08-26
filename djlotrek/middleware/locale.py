from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.http import HttpResponseRedirect
from django.middleware.locale import LocaleMiddleware
from django.urls import resolve, reverse, is_valid_path
from django.utils import translation
from django.utils.cache import patch_vary_headers


class LangBasedOnPreferences(LocaleMiddleware):

    response_redirect_class = HttpResponseRedirect

    def _get_browser_language(self, request):
        browser_language_code = request.META.get('HTTP_ACCEPT_LANGUAGE', None)
        if browser_language_code is not None:
            languages = [
                language for language in browser_language_code.split(',') if '=' not in language
            ]
            for language in languages:
                language_code = language.split('-')[0]
                return language_code

    def process_request(self, request):
        urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
        i18n_patterns_used, _ = is_language_prefix_patterns_used(urlconf)
        language = translation.get_language_from_request(request, check_path=i18n_patterns_used)
        language_from_path = translation.get_language_from_path(request.path_info)
        language_from_browser = self._get_browser_language(request)
        language_from_session = request.session.get(translation.LANGUAGE_SESSION_KEY)
        language = settings.LANGUAGE_CODE
        if i18n_patterns_used:
            if language_from_session:
                language = language_from_session
            if not language_from_session and language_from_path:
                language = language_from_path
            if not language_from_session and language_from_browser:
                language = language_from_browser
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        language_from_path = translation.get_language_from_path(request.path_info)
        urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
        i18n_patterns_used, _ = is_language_prefix_patterns_used(urlconf)
        if (response.status_code == 404 and i18n_patterns_used):
            language_path = '%s' % (request.path_info)
            path_valid = is_valid_path(language_path, urlconf)
            if not path_valid:
                for language_available in settings.LANGUAGES:
                    translation.activate(language_available[0])
                    language_path = '%s' % (request.path_info)
                    if is_valid_path(language_path, urlconf):
                        path_valid = True
                        break
                kwargs = resolve(language_path).kwargs
                url_name = resolve(language_path).url_name
                translation.activate(language)
                language_path = reverse(url_name, kwargs=kwargs)

            path_needs_slash = (
                not path_valid and (
                    settings.APPEND_SLASH and not language_path.endswith('/') and
                    is_valid_path('%s/' % language_path, urlconf)
                )
            )
            if path_needs_slash:
                language_path = language_path + '/'
            return self.response_redirect_class(language_path)

        if not (i18n_patterns_used and language_from_path):
            patch_vary_headers(response, ('Accept-Language',))
        response.setdefault('Content-Language', language)
        return response
