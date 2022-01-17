from .cache_admin import CacheAdminMiddleware
from .cache_header import CacheHeaderMiddleware
from .cache_url import UrlIgnoreCacheMiddleware


class FetchFromCacheMiddleware(
    CacheAdminMiddleware, CacheHeaderMiddleware, UrlIgnoreCacheMiddleware
):
    pass
