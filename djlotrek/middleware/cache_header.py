from .cache_admin import CacheAdminMiddleware


class CacheHeaderMiddleware(CacheAdminMiddleware):
    def process_request(self, request):
        if request.META.get('HTTP_DISABLE_CACHE', ''):
            request._cache_update_cache = False
            return None
        return super(CacheHeaderMiddleware, self).process_request(request)
