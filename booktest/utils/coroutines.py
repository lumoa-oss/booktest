import inspect


async def maybe_async_call(func, args2, kwargs):
    # Check if func itself is a coroutine function, or if it's a callable
    # object with an async __call__ method
    is_coro = inspect.iscoroutinefunction(func) or \
              inspect.iscoroutinefunction(getattr(func, '__call__', None))

    if is_coro:
        return await func(*args2, **kwargs)
    else:
        return func(*args2, **kwargs)

