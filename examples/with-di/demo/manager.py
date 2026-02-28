from sprintapi import service, Service
from sprintapi.logging import get_sprintapi_logger

from .config import DemoConfig


_logger = get_sprintapi_logger('AppManager')


@service
class AppManager(Service):
    def __init__(self, config: DemoConfig):
        self._app_name = config.app_name

    async def get_message(self):
        return f'This app is {self._app_name}.'

    async def start(self):
        _logger.info('AppManager started')

    async def stop(self):
        _logger.info('AppManager stopped')
