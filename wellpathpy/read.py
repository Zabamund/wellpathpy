import pandas as pd
import numpy as np

from .checkarrays import checkarrays

def read_csv(fname):
    """
    Read a deviation file in CSV format with a header row
    containing no less than `md`, `inc` and `azi`.
    Other columns are ignored.

    Parameters
    ----------
    fname: str, path to a CSV file with this format:
    '''
    md,inc,azi
    0,0,244
    1,11,220
    2,13,254
    3,15,254
    '''

    md: float, measured depth (units not defined)
    inc: float, well inclination in degrees from vertical
    azi: float, well azimuth in degrees from North

    Returns
    -------
    a tuple of np.ndarray of md, inc and azi

    """
    df = pd.read_csv(fname, header=0)

    md, inc, azi = df['md'].values, df['inc'].values, df['azi'].values
    md, inc, azi = checkarrays(md, inc, azi)

    return md, inc, azi