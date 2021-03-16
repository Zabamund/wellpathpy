import numpy as np

from .checkarrays import checkarrays

def read_csv(fname, delimiter=',', skiprows=1, **kwargs):
    """Read a deviation file in CSV format

    A header row containing the column names `md`, `inc`, `azi` in
    that order is generally expected to be included as the first row
    in the file. By default, this header is skipped with the `skiprows`
    argument set to `1` but this can be changed to `0` if no header is
    inclduded.
    The data must be ordered as `md`, `inc`, `azi` as the data cannot
    be distinguished numerically.

    Parameters
    ----------
    fname : str
        path to a CSV file with this format:
        ```md,inc,azi
        0,0,244
        10,11,220
        50,43,254
        150,78.5,254
        252.5,90,359.9```
    delimiter: str
        the character used as a delimiter in the CSV
    skiprows : int
        number of rows to skip, normally the header row

    Other Parameters
    ----------------
    **kwargs : All other keyword arguments are passed to `np.loadtxt`

    Returns
    -------
    md, inc, azi : tuple
        md, inc and azi are of type np.ndarray

    Notes
    -----
    md : float
        measured depth (units not defined)
    inc : float
        well inclination in degrees from vertical
    azi : float
        well azimuth in degrees from Grid North
    """
    dev = np.loadtxt(fname, delimiter=delimiter, skiprows=skiprows, **kwargs)
    md, inc, azi = np.split(dev[:,0:3], 3, 1)
    md, inc, azi = checkarrays(md, inc, azi)

    return md, inc, azi
