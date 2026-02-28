import inspect


__all__ = ['get_registry_decorator']


def get_registry_decorator(base_type: type, registry: set[type]):
    def _inner(target):
        if inspect.isfunction(target):
            return target

        if not isinstance(target, type):
            raise TypeError(f'{target} is not a type.')
        if not issubclass(target, base_type):
            raise TypeError(f'{target.__name__} is not a subclass of {base_type.__name__}.')

        if target in registry:
            raise ValueError(f'{base_type.__name__} class "{target.__name__}" is already registered.')

        registry.add(target)
        return target
    return _inner
