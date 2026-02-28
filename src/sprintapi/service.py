from .utility.type_registry import get_registry_decorator


__all__ = [
    'Service',
    'service',
    'get_service_types',
]


class Service:
    async def init(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass


_service_types: set[type[Service]] = set()

service = get_registry_decorator(Service, _service_types)

def get_service_types() -> set[type[Service]]:
    return _service_types.copy()
