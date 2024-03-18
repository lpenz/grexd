"""A console regular expression editor"""

import importlib.metadata


def version() -> str:
    return importlib.metadata.version("grexd")


__all__ = [
    "version",
]
