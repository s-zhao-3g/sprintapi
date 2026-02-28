"""
Service example for the DI demo.

`AppManager` reads configuration and provides the greeting used by the controller.
"""

from sprintapi import service, Service
from sprintapi.logging import get_sprintapi_logger

from .config import DemoConfig


_logger = get_sprintapi_logger('AppManager')


@service
class AppManager(Service):
    """
    Demo Service class implementation.

    `Service` classes are one type of server components, which has 3 lifecycles:
    - `init`: Before server startup. This typically performs DB initialization and/or loads cache;
    - `start`: During server startup.
    - `stop`: Before server shutdown.

    All lifecycle methods runs on main loop, hence resolves the issue that resource creation and usage
    are done in different async loops, which is a typical pitfall in FastAPI.

    Services are init and started in TOPOLOGICAL ORDER (in dependency graph), and stopped in reverse order.
    """

    # The constructor takes the `DemoConfig` as a parameter, which will be injected by the framework.
    def __init__(self, config: DemoConfig):
        self._app_name = config.app_name

    async def get_message(self):
        return f'This app is {self._app_name}.'

    async def init(self):
        # This is called during app initialization, before any services are started
        _logger.info('AppManager initialized')

    async def start(self):
        # This is called during app startup
        _logger.info('AppManager started')

    async def stop(self):
        # This is called before app shutdown
        _logger.info('AppManager stopped')
