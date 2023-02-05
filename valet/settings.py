"""
Handle application settings.
"""

import tomllib
import typing as tp


def load_config(path: str) -> dict[str, tp.Any]:
    """Load application's configuration from a TOML file."""
    with open(path, 'rb') as f:
        conf = tomllib.load(f)
    return conf
