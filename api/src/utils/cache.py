from hashlib import md5


def custom_key_builder(
    func,
    namespace,
    request,
    *args,
    **kwargs,
) -> str:
    """Key builder for FastAPICache.

    Uses url and request.state.user_id key to create a key for cache.

    Parameters:
        func: function  # noqa: RST213,RST210
        namespace: name of the redis space
        request: FastAPI.request
        *args: for essential library parameters
        **kwargs: for essential named library parameters

    Returns:
        str: "namespace:hashed_key"
    """
    key_str = "{path}:{user_id}".format(
        path=request.url.path,
        user_id=getattr(request.state, "user_id", None),
    )
    hashed_key = md5(
        key_str.encode(),
        usedforsecurity=False,
    ).hexdigest()

    return "{namespace}:{key}".format(namespace=namespace, key=hashed_key)
