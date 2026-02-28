from sprintapi import api_route, get_mapping, Controller

from .manager import AppManager


@api_route('/app')
class AppController(Controller):
    def __init__(self, manager: AppManager):
        self._manager = manager

    @get_mapping('name')
    async def get_app_name(self):
        return await self._manager.get_message()
