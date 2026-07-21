from django.core.cache import cache


class CacheVersion:
    """
    Generalized version-key invalidation helper — same O(1) invalidation
    pattern first built ad-hoc for catalog products in Phase 7, now
    reusable by any namespace (search, popularity, future apps).
    """
    def __init__(self, namespace: str):
        self.version_key = f"cacheversion:{namespace}"

    def get(self) -> int:
        version = cache.get(self.version_key)
        if version is None:
            cache.set(self.version_key, 1, timeout=None)
            return 1
        return version

    def bump(self) -> None:
        try:
            cache.incr(self.version_key)
        except ValueError:
            cache.set(self.version_key, 1, timeout=None)

    def make_key(self, **params) -> str:
        version = self.get()
        normalized = "&".join(f"{k}={v}" for k, v in sorted(params.items()) if v is not None)
        return f"{self.version_key.replace('cacheversion:', '')}:v{version}:{normalized}"