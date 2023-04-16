"""Dotpather is a library to help translate Python dictionaries into dot notation."""

from .builder import PathBuilder
from .differ import get_diff

__all__ = ["PathBuilder", "get_diff"]
