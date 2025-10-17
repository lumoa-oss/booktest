import inspect


async def maybe_async_call(func, args2, kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args2, **kwargs)
    else:
        return func(*args2, **kwargs)

