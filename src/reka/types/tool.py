# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from ..core.unchecked_base_model import UncheckedBaseModel


class Tool(UncheckedBaseModel):
    """
    The whole tool specification that includes the name of the tool function,
    a description, and the detailed input schema.

    An example of a tool function that returns the temperature of a city in a given unit:
    {
    "name": "get_weather_in_unit",
    "description": "Get the weather in a given location in the given unit.",
    "parameters": {
    "type": "object",
    "properties": {
    "location": {
    "type": "string",
    "description": "The city and state, e.g. San Francisco, CA"
    },
    "unit": {
    "enum": ["c", "f"],
    "description": "The unit of temperature, either 'c' (celsius) or 'f' (fahrenheit)"
    },
    }
    "required": ["location"]
    }
    }
    """

    description: typing.Optional[str] = None
    name: str
    parameters: typing.Dict[str, typing.Any]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}