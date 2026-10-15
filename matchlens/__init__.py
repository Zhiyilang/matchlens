"""MatchLens — offline explainable match-intelligence agent (zero deps)."""
from . import core
from . import generate
from . import i18n
from . import live

__version__ = "1.1.0"
__all__ = ["core", "generate", "i18n", "live", "analyze"]


def analyze(*args, **kwargs):
    return core.analyze(*args, **kwargs)
