"""Handle application settings."""

import pathlib
import tomllib


BASE_DIR = pathlib.Path(__file__).parent.parent


def load_config(path: str):
    """Load application's configuration from a TOML file."""
    with open(path, 'rb') as f:
        conf = tomllib.load(f)
    return conf
