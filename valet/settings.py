import pathlib
import tomllib


# BASE_DIR = pathlib.Path(__file__).parent.parent
# PACKAGE_NAME = 'valet'


def load_config(path):
    with open(path, 'rb') as f:
        conf = tomllib.load(f)
    return conf
