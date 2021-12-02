from django.conf import settings
from django.middleware.cache import UpdateCacheMiddleware
import re 


# This removes cache from certain url. The list of exceptions can be provided using CACHE_MIDDLEWARE_IGNORE setting also via regex.
class UrlIgnoreCacheMiddleware(UpdateCacheMiddleware):
    def process_response(self, request, response):
        full_path = request.get_full_path()
        ignores = getattr(settings, 'CACHE_MIDDLEWARE_IGNORE', [])
        if isinstance(ignores, str):
            ignores = [ignores] 
        for ignore in ignores:
            if re.match(ignore, full_path):
                return response
        return super(UrlIgnoreCacheMiddleware, self).process_response(
            request, response
        )