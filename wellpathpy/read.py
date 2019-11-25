import pandas as pd

from .checkarrays import checkarrays

def read_csv(fname, md = 'md', inc = 'inc', azi = 'azi', **kwargs):
    """Read a deviation file in CSV format

    Read a deviation survey from a CSV file. Columns can be specified with the
    md, inc, and azi parameters.

    Parameters
    ----------
    fname : str
        path to a CSV file with this format:
    md : str
        measured depth column name
    inc : str
        inclination column name
    azi : str
        azimuth column name

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
        well azimuth in degrees from North
    """
    df = pd.read_csv(fname, header=0, **kwargs)

    md, inc, azi = df[md].values, df[inc].values, df[azi].values
    md, inc, azi = checkarrays(md, inc, azi)

    return md, inc, azi
