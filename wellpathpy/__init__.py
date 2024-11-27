import sys
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

try:
    __version__ = metadata.version(__name__)
except: # PackageNotFoundError
    # Don't hard crash when the the version cannot be looked up from the
    # metadata, probably because the tests are running from the source dir and
    # the module has not been packaged yet.
    pass

__all__ = [
    'read_header_json',
    'read_csv',
    'deviation_to_csv',
    'position_to_csv',
    'deviation',
    'position_log',
    'minimum_curvature'
]

from .header import read_header_json
from .read import read_csv
from .write import deviation_to_csv, position_to_csv
from .position_log import deviation, position_log, minimum_curvature
