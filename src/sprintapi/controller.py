import fastapi
import inspect


__all__ = [
    'api_route',
    'get_controller_types',
    'Controller',

    'get_mapping',
    'post_mapping',
    'put_mapping',
    'delete_mapping'
]


# APIs


def _method_mapping(method: str, route: str, **kwargs):
    if not route.startswith('/') and len(route) > 0:
        route = '/' + route

    def _inner(target):
        if not inspect.isfunction(target):
            return target

        target._sprint_api_type = method
        target._sprint_api_route = route
        target._sprint_api_args = kwargs

        return target

    return _inner


def get_mapping(route: str, **kwargs):
    if not isinstance(route, str):
        raise ValueError('Route is not specified.')
    return _method_mapping('GET', route, **kwargs)


def post_mapping(route: str, **kwargs):
    if not isinstance(route, str):
        raise ValueError('Route is not specified.')
    return _method_mapping('POST', route, **kwargs)


def put_mapping(route: str, **kwargs):
    if not isinstance(route, str):
        raise ValueError('Route is not specified.')
    return _method_mapping('PUT', route, **kwargs)


def delete_mapping(route: str, **kwargs):
    if not isinstance(route, str):
        raise ValueError('Route is not specified.')
    return _method_mapping('DELETE', route, **kwargs)


# Controllers


class Controller:
    def get_router(self):
        route_prefix = getattr(self, '_sprint_api_route', '')
        args = getattr(self, '_sprint_api_args', {})

        router = fastapi.APIRouter(prefix=route_prefix, **args)

        for method_name in dir(self):
            if method_name.startswith('__'):
                continue

            method = getattr(self, method_name)
            if not callable(method):
                continue

            api_type = getattr(method, '_sprint_api_type', None)
            route = getattr(method, '_sprint_api_route', None)
            args = getattr(method, '_sprint_api_args', {})

            if api_type is None or route is None:
                continue

            if api_type in ('GET', 'POST', 'PUT', 'DELETE'):
                router.api_route(path=route, methods=[api_type], **args)(method)

        return router


_controller_types: set[type[Controller]] = set()


def api_route(route: str, **kwargs):
    if not isinstance(route, str):
        raise ValueError('Route is not specified.')

    if route.endswith('/'):
        route = route[:-1]

    global _controller_types

    def _inner(target):
        if inspect.isfunction(target):
            return target

        if not isinstance(target, type):
            raise TypeError(f'{target} is not a type.')
        if not issubclass(target, Controller):
            raise TypeError(f'{target.__name__} is not a subclass of Controller.')

        if target in _controller_types:
            raise ValueError(f'Controller class "{target.__name__}" is already registered.')

        _controller_types.add(target)
        target._sprint_api_route = route
        target._sprint_api_args = kwargs

        return target

    return _inner


def get_controller_types() -> set[type[Controller]]:
    return _controller_types.copy()
