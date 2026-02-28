import inspect
from collections import defaultdict, deque
from typing import Any, Callable, Iterable, get_type_hints


__all__ = ['DependencyContainer']


class DependencyContainer:
    def __init__(self):
        self._components: dict[type, tuple[Callable, bool]] = {}
        self._singletons: dict[type, object] = {}

    def check_circular(self):
        # build indegree map with all related deps
        indegree_map = self._build_indegree_map(self._components.keys())

        unresolved = deque([c for c, count in indegree_map.items() if count == 0])
        visit_count = 0

        while unresolved:
            interface = unresolved.popleft()
            visit_count += 1

            deps = list(self._get_direct_deps(interface).values())
            for dep in deps:
                indegree_map[dep] -= 1
                if indegree_map[dep] == 0:
                    unresolved.append(dep)

        return visit_count != len(indegree_map)

    def register(self, interface: type[object], impl: Callable, is_singleton: bool = False):
        if interface in self._components:
            raise TypeError(f'Type "{interface.__name__}" already registered."')
        self._components[interface] = (impl, is_singleton)

    def resolve(self, interface: type):
        deps = self._get_direct_deps(interface)
        dep_impls = {k: self.resolve(v) for k, v in deps.items()}
        impl_info = self._components.get(interface, None)

        if impl_info is None:
            raise TypeError(f'Failed to resolve dependency of type: "{interface.__name__}".')

        impl, is_singleton = impl_info
        if is_singleton:
            if interface not in self._singletons:
                self._singletons[interface] = self._create_impl(interface, impl, dep_impls)
            return self._singletons[interface]
        return self._create_impl(interface, impl, dep_impls)

    def resolve_with_order(self, interfaces: Iterable[type]) -> list[Any]:
        target_interfaces = set(interfaces)

        # find all related interfaces along the path
        related_interfaces = set()
        unresolved = deque(target_interfaces)

        while unresolved:
            interface = unresolved.popleft()
            related_interfaces.add(interface)
            for dep in self._get_direct_deps(interface).values():
                if dep not in related_interfaces:
                    unresolved.append(dep)

        indegree_map = self._build_indegree_map(related_interfaces)

        # start from no deps, simulate population, append node only if indegree depleted (Kahn's algo)
        unresolved = deque([c for c, count in indegree_map.items() if count == 0])
        res_interfaces = []

        while unresolved:
            interface = unresolved.popleft()

            if interface in target_interfaces:
                res_interfaces.append(interface)

            for dep in self._get_direct_deps(interface).values():
                indegree_map[dep] -= 1
                if indegree_map[dep] == 0:
                    unresolved.append(dep)

        return [self.resolve(interface) for interface in res_interfaces[::-1]]

    def _build_indegree_map(self, interfaces: Iterable[type]) -> dict[type, int]:
        indegree_map = defaultdict(int)
        for c in interfaces:
            indegree_map[c] += 0
            for dep in self._get_direct_deps(c).values():
                indegree_map[dep] += 1
        return indegree_map

    @staticmethod
    def _create_impl(interface, impl, deps):
        try:
            return impl(**deps)
        except TypeError:
            raise TypeError(f'Failed to resolve dependency of type: "{interface.__name__}".')

    def _get_direct_deps(self, interface: type) -> dict[str, type]:
        impl_info = self._components.get(interface, None)
        if not impl_info:
            raise TypeError(f'Failed to resolve dependency of type: "{interface.__name__}".')

        impl_sig, _ = impl_info
        if inspect.isclass(impl_sig):
            type_hints = get_type_hints(impl_sig.__init__)
        else:
            type_hints = get_type_hints(impl_sig)

        return { name: pt for name, pt in type_hints.items() if name != 'return' }
