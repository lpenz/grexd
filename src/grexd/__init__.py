"""A console regular expression editor"""

import importlib.metadata

from .hugefilevieweruicontrol import HugeFileViewerUIControl


def version() -> str:
    return importlib.metadata.version("grexd")


__all__ = [
    "version",
    "HugeFileViewerUIControl",
]
