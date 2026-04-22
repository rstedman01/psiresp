import pytest
import numpy as np

import psiresp
from psiresp.base import Model
from psiresp.base import _to_immutable


@pytest.mark.parametrize("object_in, object_out", [
    (np.ones(3), (1, 1, 1)),
    (np.zeros((2, 2)), ((0, 0), (0, 0))),  # recursive list
    ({1, 2, 3}, frozenset({1, 2, 3})),
    (
        [{'key': {'key3': 3, 'key2': {1, 2}}}],
        ((('key', (('key2', frozenset({1, 2})), ('key3', 3))),),)
    )
])
def test_to_immutable(object_in, object_out):
    immuted = _to_immutable(object_in)
    assert immuted == object_out
    hash(immuted)


class _SetModel(Model):
    values: set[int]


def test_hash_with_set_field():
    model = _SetModel(values={1, 2, 3})
    assert isinstance(model.get_hash(), str)
    assert len(model.get_hash()) == 40


def test_package_version_is_available():
    assert isinstance(psiresp.__version__, str)
