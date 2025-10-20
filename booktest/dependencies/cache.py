from collections import OrderedDict


class LruCache:
    # This can be provided as the memory cache to avoid
    # running out of memory during the test

    def __init__(self, size: int):
        self.__cache = OrderedDict()
        self.__size = size

    def __len__(self):
        return len(self.__cache)

    def __contains__(self, key):
        return key in self.__cache

    def __getitem__(self, key):
        if key not in self.__cache:
            return None
        else:
            self.__cache.move_to_end(key)
            return self.__cache[key]

    def __setitem__(self, key, value) -> None:
        if key is None:
            # if we are storing None: let's erase old value, if available
            old = self.__cache.get(key)
            if old is not None:
                del self.__cache[key]
        else:
            self.__cache[key] = value
            self.__cache.move_to_end(key)
            if len(self.__cache) > self.__size:
                self.__cache.popitem(last=False)


class NoCache:
    # This can be provided to skip using in-memory cache
    # as in-memory cache may lead to memory usage issues.

    def __len__(self):
        return 0

    def __getitem__(self, key):
        return None

    def __setitem__(self, key, value) -> None:
        pass

