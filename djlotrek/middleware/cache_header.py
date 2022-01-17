from django.middleware.cache import FetchFromCacheMiddleware


class CacheHeaderMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):
        if request.META.get("HTTP_DISABLE_CACHE", False):
            request._cache_update_cache = False
            return None
        return super(CacheHeaderMiddleware, self).process_request(request)
