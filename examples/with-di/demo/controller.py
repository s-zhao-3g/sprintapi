"""
Controller example for the DI demo.

Exposes a small API that returns the configured app name via `AppManager`.
"""

from sprintapi import api_route, get_mapping, Controller

from .manager import AppManager


@api_route('/app')
class AppController(Controller):
    # Constructor that takes the AppManager as a dependency, which will be injected by the framework
    # Make sure to type-annotate the parameter so SprintAPI knows what to inject
    def __init__(self, manager: AppManager):
        self._manager = manager

    # Simple GET endpoint that returns the app name from the manager
    @get_mapping('name')
    async def get_app_name(self):
        return await self._manager.get_message()
