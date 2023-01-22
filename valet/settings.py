"""Handle application settings."""

import tomllib


def load_config(path: str):
    """Load application's configuration from a TOML file."""
    with open(path, 'rb') as f:
        conf = tomllib.load(f)
    return conf
