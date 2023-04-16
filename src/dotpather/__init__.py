"""Dotpather is a library to help translate Python dictionaries into dot notation."""

from .builder import build_paths
from .differ import get_diff

__all__ = ["build_paths", "get_diff"]
