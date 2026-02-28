from .utility.type_registry import get_registry_decorator


__all__ = [
    'AsyncService',
    'Service',

    'async_service',
    'service',

    'get_async_service_types',
    'get_service_types',
]


class AsyncService:
    async def init(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass


class Service:
    def init(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


_async_service_types: set[type[AsyncService]] = set()
_service_types: set[type[Service]] = set()

async_service = get_registry_decorator(AsyncService, _async_service_types)
service = get_registry_decorator(Service, _service_types)


def get_async_service_types() -> set[type[AsyncService]]:
    return _async_service_types.copy()


def get_service_types() -> set[type[Service]]:
    return _service_types.copy()
