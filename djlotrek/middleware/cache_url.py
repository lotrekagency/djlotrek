from django.conf import settings
from django.middleware.cache import FetchFromCacheMiddleware
import re


# This removes cache from certain url. The list of exceptions can be provided using CACHE_MIDDLEWARE_IGNORE setting also via regex.
class UrlIgnoreCacheMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):
        full_path = request.get_full_path()
        ignores = getattr(settings, "CACHE_MIDDLEWARE_IGNORE", [])
        if isinstance(ignores, str):
            ignores = [ignores]
        for ignore in ignores:
            if re.match(ignore, full_path):
                request._cache_update_cache = False
                return None
        return super(UrlIgnoreCacheMiddleware, self).process_request(request)
