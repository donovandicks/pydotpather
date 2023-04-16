import pytest

from dotpather import PathBuilder


@pytest.fixture
def pb():
    return PathBuilder()
