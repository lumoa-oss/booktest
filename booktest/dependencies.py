import abc
import functools
import inspect
from typing import Optional

from booktest.coroutines import maybe_async_call

#
# The way how resources should work, is that we have a resources like
#
# - port pool between 10000 and 20000
# - RAM pool with 4 GB of RAM
#
# We can allocate a resource from the pool, and then deallocate it
#
# - e.g. we can request a port from the pool, and then deallocate it
# - or we can request a GB from GB pool and then deallocate it
#
# Because the need for multiprocessing, we need to be able to preallocate resources
#
# - e.g. we can preallocate a port from the pool in main process for a subprocess
#
# Now, in order to be able to keep track of allocations and preallocations, we
# need to have e.g. set for allocated resources, and a map for preallocated resources
#
# - preallocated map should likely be from (case_id, resource_id) to allocation_id
#   - e.g. (book/app/test, port) -> 10024
# - allocation set should likely just likely be a (resource_id, allocation_id) set
#
# On allocation, we receive allocations and preallocations and return allocation_idq
#

class Allocator(abc.ABC):
    """
    Allocators are used to allocate resources for tests.

    The big theme with python testing is that in parallel runs, resources need to preallocated
    in main thread, before these resource allocations get passed to the actual test cases.
    """

    @property
    @abc.abstractmethod
    def identity(self):
        """
        The identity of the resource. This needs to be something that can be stored in a set
        """
        pass

    @abc.abstractmethod
    def allocate(self, allocations: set[tuple], preallocations: dict[any, any]) -> Optional[any]:
        """
        Allocates a resource and returns it. If resource cannot be allocated, returns None.

        allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these
        preallocated resources - is a map from identity to resource. use these to guide allocation
        """
        pass


class Resource(Allocator):
    """
    Represents an exclusive resources, which must not be
    shared simultaneously by several parallel tests

    Such a resource can be a specific port, file system resource,
    some global state or excessive use of RAM or GPU, that prohibits parallel
    run.
    """

    def __init__(self, value, identity=None):
        self.value = value
        if identity is None:
            identity = value
        self._identity = identity

    @property
    def identity(self):
        """
        The identity of the resource
        """
        return self._identity

    def allocate(self, allocations: set[tuple], preallocations: dict[any, any]) -> any:
        """
        Allocates a resource and returns it
        :return:
        """
        if (self.identity, self.value) not in allocations:
            return self.value
        else:
            return None

    def __eq__(self, other):
        return isinstance(other, Resource) and self.identity == other.identity

    def __hash__(self):
        return hash(self.identity)

    def __repr__(self):
        if self.identity:
            return str(self.identity)
        else:
            return str(self.value)


class Pool(Allocator):
    """
    A pool of resource like ports, that must not be used simultaneously.
    """

    def __init__(self, identity, resources):
        self._identity = identity
        self.resources = resources

    @property
    def identity(self):
        """
        The identity of the resource
        """
        return self._identity

    def allocate(self, allocations: set[tuple], preallocations: dict[any, any]) -> any:
        rv = preallocations.get(self._identity)

        if rv is None:
            for i in self.resources:
                entry = (self.identity, i)
                if entry not in allocations:
                    rv = i
                    break

        return rv

def port_range(begin: int, end:int):
    return Pool("port", list(range(begin, end)))

def port(value: int):
    """
    Generates a resource for given port.
    A special identifier is generated in order to not mix the port
    with other resource integers
    """
    return port_range(value, value + 1)

def get_decorated_attr(method, attr):
    while True:
        if hasattr(method, attr):
            return getattr(method, attr)
        if hasattr(method, "_original_function"):
            method = method._original_function
        else:
            return None


def remove_decoration(method):
    while hasattr(method, "_original_function"):
        method = method._original_function
    return method


def bind_dependent_method_if_unbound(method, dependency):
    dependency_type = get_decorated_attr(dependency, "_self_type")
    self = get_decorated_attr(method, "__self__")

    if dependency_type is not None and self is not None and isinstance(self, dependency_type):
        return dependency.__get__(self, self.__class__)
    else:
        return dependency

def release_dependencies(dependencies, resolved, allocations):
    """
    Releases all dependencies
    """
    for dependency, resource in zip(dependencies, resolved):
        if isinstance(dependency, Allocator):
            entry = (dependency.identity, resource)
            allocations.remove(entry)


async def call_class_method_test(dependencies, func, self, case, kwargs):
    run = case.run

    resolved = []
    allocations = run.allocations

    for dependency in dependencies:
        if isinstance(dependency, Allocator):
            resource = dependency.allocate(allocations, run.preallocations)
            allocations.add((dependency.identity, resource))
            resolved.append(resource)
        else:
            unbound_method = dependency
            # 1. Try first to find this method for this exact test instance.
            #    This covers cases, where a test class has been instantiated
            #    with several different parameters

            bound_method = unbound_method.__get__(self, self.__class__)
            found, result = \
                run.get_test_result(
                    case,
                    bound_method)

            # 2. If method is not exist for test instance, try to look elsewhere.
            #    This allows for tests to share same data or prepared model
            if not found:
                found, result = \
                    run.get_test_result(
                        case,
                        unbound_method)

            if not found:
                raise ValueError(f"could not find or make method {unbound_method} result")

            resolved.append(result)

    args2 = []
    args2.append(self)
    args2.append(case)
    args2.extend(resolved)

    rv = await maybe_async_call(func, args2, kwargs)

    release_dependencies(dependencies, resolved, allocations)

    return rv


async def call_function_test(dependencies, func, case, kwargs):
    run = case.run

    resolved = []
    allocations = run.allocations

    for dependency in dependencies:
        if isinstance(dependency, Allocator):
            resource = dependency.allocate(allocations, run.preallocations)
            allocations.add((dependency.identity, resource))
            resolved.append(resource)
        else:
            found, result = \
                run.get_test_result(
                    case,
                    dependency)

            if not found:
                raise ValueError(f"could not find or make method {dependency} result")

            resolved.append(result)

    args2 = []
    args2.append(case)
    args2.extend(resolved)

    rv = await maybe_async_call(func, args2, kwargs)

    release_dependencies(dependencies, resolved, allocations)

    return rv


def depends_on(*dependencies):
    """
    This method depends on a method on this object.
    """
    methods = []
    resources = []
    for i in dependencies:
        if isinstance(i, Allocator):
            resources.append(i)
        else:
            methods.append(i)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook

            if isinstance(args[0], TestBook):
                return await call_class_method_test(dependencies, func, args[0], args[1], kwargs)
            else:
                return await call_function_test(dependencies, func, args[0], kwargs)

        wrapper._dependencies = methods
        wrapper._resources = resources
        wrapper._original_function = func
        return wrapper

    return decorator

