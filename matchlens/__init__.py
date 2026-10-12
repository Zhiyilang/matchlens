"""MatchLens — offline explainable match-intelligence agent (zero deps)."""
from . import core

__version__ = "1.0.0"
__all__ = ["core", "analyze"]


def analyze(*args, **kwargs):
    return core.analyze(*args, **kwargs)
