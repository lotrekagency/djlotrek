from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.middleware.locale import LocaleMiddleware
from django.urls import resolve, reverse, is_valid_path
from django.utils import translation
from django.utils.cache import patch_vary_headers


class LangBasedOnPreferences(LocaleMiddleware):

    def _disabled(self, request):
        language = translation.get_language()
        disabled_views = getattr(settings, "LANG_ON_PREFERENCE_DISABLED_VIEWS", [])
        need_standard = False
        for language_available in settings.LANGUAGES:
            translation.activate(language_available[0])
            try:
                need_standard = resolve(request.path_info).url_name in disabled_views
            except:  # NOQA
                pass
        translation.activate(language)
        return need_standard

    def process_request(self, request):
        if self._disabled(request):
            setattr(request, "language_on_settings", False)
            return super().process_request(request)
        else:
            setattr(request, "language_on_settings", True)
        urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
        i18n_patterns_used, _ = is_language_prefix_patterns_used(urlconf)
        language = translation.get_language_from_request(
            request, check_path=i18n_patterns_used
        )
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        if not request.language_on_settings:
            return super().process_response(request, response)
        language = translation.get_language()
        language_from_path = translation.get_language_from_path(request.path_info)
        urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
        i18n_patterns_used, _ = is_language_prefix_patterns_used(urlconf)
        if (
            language != language_from_path
            and response.status_code == 404
            and i18n_patterns_used
        ):
            language_path = old_path = "%s" % (request.path_info)
            path_valid = is_valid_path(language_path, urlconf)
            if not path_valid:
                for language_available in settings.LANGUAGES:
                    translation.activate(language_available[0])
                    language_path = "%s" % (request.path_info)
                    if is_valid_path(language_path, urlconf):
                        path_valid = True
                        break
                kwargs = resolve(language_path).kwargs
                url_name = resolve(language_path).url_name
                translation.activate(language)
                language_path = reverse(url_name, kwargs=kwargs)

            path_needs_slash = not path_valid and (
                settings.APPEND_SLASH
                and not language_path.endswith("/")
                and is_valid_path("%s/" % language_path, urlconf)
            )
            if path_needs_slash:
                language_path = language_path + "/"
            if old_path != language_path:
                return self.response_redirect_class(language_path)

        if not (i18n_patterns_used and language_from_path):
            patch_vary_headers(response, ("Accept-Language",))
        response.setdefault("Content-Language", language)
        return response
