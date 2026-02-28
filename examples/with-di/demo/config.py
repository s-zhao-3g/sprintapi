from pydantic import Field
from sprintapi import Configuration, configuration

@configuration
class DemoConfig(Configuration):
    app_name: str = Field(alias='APP_NAME', default='SprintApiDemo')
