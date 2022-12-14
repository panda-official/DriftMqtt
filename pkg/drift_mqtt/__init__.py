""" MQTT Tools
"""


from .client import Client

__all__ = ["Client"]


def _load_version() -> str:
    """Load version from VERSION file"""
    from pathlib import Path  # pylint: disable=import-outside-toplevel

    here = Path(__file__).parent
    with open(here / "VERSION", "r", encoding="utf-8") as version_file:
        return version_file.read().strip()


__version__ = _load_version()
