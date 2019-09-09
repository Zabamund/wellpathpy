import pandas as pd

from .checkarrays import checkarrays

def read_csv(fname):
    """Read a deviation file in CSV format

    Parameters
    ----------
    fname : str
        path to a CSV file with this format:

    Notes
    -----
    required column names: md, inc, azi

    md : float
        measured depth (units not defined)
    inc : float
        well inclination in degrees from vertical
    azi : float
        well azimuth in degrees from North

    The columns md, inc, azi **must** be passed in this order,
    Other columns are ignored.

    Returns
    -------
    md, inc, azi : tuple
        md, inc and azi are of type np.ndarray

    """
    df = pd.read_csv(fname, header=0)

    md, inc, azi = df['md'].values, df['inc'].values, df['azi'].values
    md, inc, azi = checkarrays(md, inc, azi)

    return md, inc, azi