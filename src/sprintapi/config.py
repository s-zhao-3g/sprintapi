import os

from pydantic import BaseModel
from typing import Any, Mapping

from .utility.type_registry import get_registry_decorator


__all__ = [
    'Configuration',
    'configuration',
    'get_configuration_types',
]


class Configuration(BaseModel):
    @classmethod
    def load(cls):
        config_dict = cls._get_required_dict(os.environ)
        return cls.model_validate(config_dict, by_alias=True)

    @classmethod
    def _get_required_dict(cls, d: Mapping[str, Any]):
        res = {}
        for key in cls.model_json_schema()['properties']:
            if key in d:
                res[key] = d[key]
        return res


_config_types: set[type[Configuration]] = set()
configuration = get_registry_decorator(Configuration, _config_types)


def get_configuration_types() -> set[type[Configuration]]:
    return _config_types.copy()
