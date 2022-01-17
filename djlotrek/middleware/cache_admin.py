from django.middleware.cache import FetchFromCacheMiddleware


class CacheAdminMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):
        user = getattr(request, "user", None)
        if user and user.is_superuser:
            request._cache_update_cache = False
            return None
        return super(CacheAdminMiddleware, self).process_request(request)
