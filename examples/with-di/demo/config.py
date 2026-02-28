"""
Configuration model for the DI demo.
"""

from pydantic import Field
from sprintapi import Configuration, configuration

@configuration
class DemoConfig(Configuration):
    """
    Reads `APP_NAME` from the environment.

    Since `Configuration` class is derived from pydantic `BaseModel`,
    you can use Pydantic features like field validation,
    default values, and aliases.
    """
    app_name: str = Field(alias='APP_NAME', default='SprintApiDemo')
