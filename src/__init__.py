import tomllib

with open("pyproject.toml", "rb") as f:
    _META = tomllib.load(f)

VERSION = _META["project"]["version"]
