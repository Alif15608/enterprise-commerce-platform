from django.core.cache import cache

PRODUCT_LIST_VERSION_KEY = "catalog:products:version"
CATEGORY_TREE_VERSION_KEY = "catalog:categories:version"
DEFAULT_CACHE_TTL = 60 * 15  # 15 minutes


def get_products_cache_version():
    version = cache.get(PRODUCT_LIST_VERSION_KEY)
    if version is None:
        cache.set(PRODUCT_LIST_VERSION_KEY, 1, timeout=None)
        return 1
    return version


def bump_products_cache_version():
    """
    Called on any product create/update/delete. Increments the version
    so every previously cached list/detail response key becomes stale
    and unreachable — O(1), no key scanning required.
    """
    try:
        cache.incr(PRODUCT_LIST_VERSION_KEY)
    except ValueError:
        cache.set(PRODUCT_LIST_VERSION_KEY, 1, timeout=None)


def get_categories_cache_version():
    version = cache.get(CATEGORY_TREE_VERSION_KEY)
    if version is None:
        cache.set(CATEGORY_TREE_VERSION_KEY, 1, timeout=None)
        return 1
    return version


def bump_categories_cache_version():
    try:
        cache.incr(CATEGORY_TREE_VERSION_KEY)
    except ValueError:
        cache.set(CATEGORY_TREE_VERSION_KEY, 1, timeout=None)


def make_product_list_cache_key(query_params: dict) -> str:
    version = get_products_cache_version()
    normalized = "&".join(f"{k}={v}" for k, v in sorted(query_params.items()))
    return f"products:list:v{version}:{normalized}"


def make_category_tree_cache_key() -> str:
    version = get_categories_cache_version()
    return f"categories:tree:v{version}"