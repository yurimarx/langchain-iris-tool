from importlib import metadata

from langchain_iris_tool.tools import InterSystemsIRISTool

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = "0.0.1"
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "InterSystemsIRISTool",
    "__version__",
]