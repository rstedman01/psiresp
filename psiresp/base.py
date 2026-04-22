import inspect
import hashlib
import json
from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict, ValidationError


def _is_settable(member):
    return isinstance(member, property) and member.fset is not None


def _to_immutable(obj):
    if isinstance(obj, np.ndarray):
        obj = obj.tolist()
    if isinstance(obj, set):
        return frozenset(obj)
    elif isinstance(obj, list):
        return tuple(_to_immutable(x) for x in obj)
    elif isinstance(obj, dict):
        return tuple((k, _to_immutable(v)) for k, v in sorted(obj.items()))
    return obj


class Model(BaseModel):
    """Base class that all classes should subclass.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        json_encoders={np.ndarray: lambda x: x.tolist()},
    )

    @property
    def _clsname(self):
        return type(self).__name__

    def __pre_init__(self, **kwargs):
        pass

    def __post_init__(self, **kwargs):
        pass

    def model_post_init(self, __context: Any) -> None:
        self.__post_init__()

    def __setattr__(self, attr, value):
        try:
            super().__setattr__(attr, value)
        except (ValueError, ValidationError) as e:
            setters = inspect.getmembers(self.__class__, predicate=_is_settable)
            for propname, _ in setters:
                if propname == attr:
                    return object.__setattr__(self, propname, value)
            raise e

    def get_hash(self):
        def _fallback(value):
            if hasattr(value, "model_dump_json"):
                return json.loads(value.model_dump_json())
            if hasattr(value, "json"):
                return json.loads(value.json())
            return str(value)

        mash = hashlib.sha1()
        mash.update(self.model_dump_json(fallback=_fallback).encode("utf-8"))
        return mash.hexdigest()

    def __hash__(self):
        return hash(self.get_hash())

    def __eq__(self, other):
        try:
            other_hash = hash(other)
        except TypeError:
            other_hash = hash(_to_immutable(other))
        return hash(self) == other_hash
