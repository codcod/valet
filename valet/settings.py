"""
Handle application settings.
"""

import os
import pathlib
import tomllib
import typing as tp

BASE_DIR = pathlib.Path(__file__).parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {name} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{asctime} - {name}:{module} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'valet.log',
            'formatter': 'verbose',
            'level': 'DEBUG',
            'mode': 'w',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.getenv('VALET_LOG_LEVEL', 'DEBUG'),
    },
    'loggers': {
        'asyncio': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'adev.server.dft': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'aiosqlite': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'watchgod.main': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}


def load_config(path: str) -> dict[str, tp.Any]:
    """Load application's configuration from a TOML file."""
    with open(path, 'rb') as f:
        conf = tomllib.load(f)
    return conf
