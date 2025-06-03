import abc
import copy
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

class ResourceAllocator(abc.ABC):
    """
    Allocators are used to allocate resources for tests.

    The big theme with python testing is that in parallel runs, resources need to preallocated
    in main thread, before these resource allocations get passed to the actual test cases.
    """

    @abc.abstractmethod
    def allocate(self, allocation_id: any, allocations: set[tuple], preallocations: dict[any, any]) -> (any, set[tuple], dict[any, any]):
        pass

    @abc.abstractmethod
    def deallocate(self, allocations: set[tuple], allocation) -> set[tuple]:
        pass


class SingleResourceAllocator(ResourceAllocator):
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

    def allocate(self, allocation_id: any, allocations: set[tuple], preallocations: dict[any, any]) -> (any, set[(any, any)], dict[any, (any, any)]):
        """
        Allocates a resource and returns it. If resource cannot be allocated, returns None.

        allocation_id - unique identifier for this allocation, used for preallocations
        allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these
        preallocated resources - is a map from allocation_name to resource. use these to guide allocation
        """
        preallocation_key = allocation_id
        identity_allocation = preallocations.get(preallocation_key)

        if identity_allocation is not None:
            allocation = identity_allocation[1]
            preallocations2 = copy.copy(preallocations)
        else:
            allocation = self.do_allocate(allocations)
            preallocations2 = copy.copy(preallocations)
            preallocations2[allocation_id] = (self.identity, allocation)

        if allocation is None:
            return None

        allocations2 = copy.copy(allocations)
        allocations2.add((self.identity, allocation))

        return allocation, allocations2, preallocations2

    def deallocate(self, allocations: set[tuple], allocation) -> set[tuple]:
        """
        Deallocates a resource and returns it. If resource cannot be deallocated, returns None.

        allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these
        allocation - is the allocation to deallocate
        """
        rv = copy.copy(allocations)
        rv.remove((self.identity, allocation))
        return rv

    @abc.abstractmethod
    def do_allocate(self, allocations: set[tuple]) -> Optional[any]:
        """
        Allocates a resource and returns it. If resource cannot be allocated, returns None.

        allocation_name - unique name for this allocation, that for preallocations
        allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these
        preallocated resources - is a map from allocation_name to resource. use these to guide allocation
        """
        pass


class Resource(SingleResourceAllocator):
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

    def do_allocate(self, allocations: set[tuple]) -> any:
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


class Pool(SingleResourceAllocator):
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

    def do_allocate(self, allocations: set[tuple]) -> any:
        for i in self.resources:
            entry = (self.identity, i)
            if entry not in allocations:
                return i

        return None

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

def release_dependencies(name, dependencies, resolved, allocations):
    """
    Releases all dependencies
    """
    for dependency, resource in zip(dependencies, resolved):
        if isinstance(dependency, ResourceAllocator):
            allocations = dependency.deallocate(allocations, resource)

    return allocations


async def call_test(method_caller, dependencies, func, case, kwargs) :
    run = case.run

    resolved = []
    allocations = run.allocations
    preallocations = run.preallocations

    name = case.test_path
    resource_pos = 0

    for dependency in dependencies:
        if isinstance(dependency, ResourceAllocator):
            allocation_id = (name, resource_pos)
            resource, allocations, _ = dependency.allocate(allocation_id, allocations, preallocations)
            allocations.add((dependency.identity, resource))
            resolved.append(resource)
            resource_pos += 1
        else:
            resolved.append(method_caller(dependency))

    args2 = []
    args2.append(case)
    args2.extend(resolved)

    rv = await maybe_async_call(func, args2, kwargs)

    run.allocations = release_dependencies(name, dependencies, resolved, allocations)

    return rv


async def call_class_method_test(dependencies, func, self, case, kwargs):

    def class_method_caller(dependency):
        run = case.run
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

        return result

    async def func2(*args2, **kwargs):
        args3 = []
        args3.append(self)
        args3.extend(args2)
        return await maybe_async_call(func, args3, kwargs)

    return await call_test(class_method_caller, dependencies, func2, case, kwargs)


async def call_function_test(dependencies, func, case, kwargs):

    def function_method_caller(dependency):
        found, result = \
            case.run.get_test_result(
                case,
                dependency)

        if not found:
            raise ValueError(f"could not find or make method {dependency} result")

        return result

    return await call_test(function_method_caller, dependencies, func, case, kwargs)


def depends_on(*dependencies):
    """
    This method depends on a method on this object.
    """
    methods = []
    resources = []
    for i in dependencies:
        if isinstance(i, ResourceAllocator):
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

