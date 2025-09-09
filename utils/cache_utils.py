from functools import wraps

from django.core.cache import cache
from rest_framework.response import Response


def cache_api(timeout=300, prefix="api"):
    def decorator(api_view):
        @wraps(api_view)
        def wrapper(request, *args, **kwargs):
            if request.method != "GET":
                return api_view(request, *args, **kwargs)
            key = generate_cache_key(
                prefix,
                request.path,
                str(request.GET.dict()),
                str(request.user.id) if request.user.is_authenticated else None,
            )

            response_cache = cache.get(key)
            if response_cache:
                return Response(response_cache)
            response = api_view(request, *args, **kwargs)
            if response.status_code == 200:
                cache.set(key, response.data, timeout=timeout)
            return response

        return wrapper

    return decorator


def generate_cache_key(prefix="api", url="api/", query_params={}, user_id=None):
    key = [prefix, url, str(query_params)]
    if user_id is not None:
        key.append(user_id)

    return ":".join(key)
