import pandas as pd

from .checkarrays import checkarrays, checkarrays_tvd

def deviation_to_csv(fname, md, inc, azi):
    """
    Write a log to a comma-separated values (csv) file.

    Parameters
    ----------
    fname: str or file handle
        file path or object the CSV will be written to.
    md: array-like,
        measured depth, unit unaware
    inc: array-like,
        inclination from vertical,
        unit unaware
    azi: array-like,
        azimuth from north,
        unit unaware

    Notes
    -----
    This function is totally unit unaware, the user is responsible
    to handle units, for example with the unit_convert function.
    Caution: to_csv uses Python write mode set to the default: ‘w’
    therefore existing files will be overwritten.

    Returns
    -------
        None
    """

    md, inc, azi = checkarrays(md, inc, azi)

    data = {
        'md': md,
        'inc': inc,
        'azi': azi
    }
    df = pd.DataFrame(data=data)
    df.to_csv(fname)

    return None

def position_to_csv(fname, depth, northing, easting):
    """
    Write a log to a comma-separated values (csv) file.

    Parameters
    ----------
    fname: str or file handle
        file path or object the CSV will be written to.
    depth: array-like,
        true vertical depth (tvd) or
        true vertical depth subsea (tvdss),
        unit unaware
    northing: array-like,
        distance north of reference point,
        unit unaware
    easting: array-like,
        distance east of reference point,
        unit unaware

    Notes
    -----
    This function is totally unit unaware, the user is responsible
    to handle units, for example with the unit_convert function.
    Caution: to_csv uses Python write mode set to the default: ‘w’
    therefore existing files will be overwritten.

    Returns
    -------
        None
    """

    depth, northing, easting = checkarrays_tvd(depth, northing, easting)

    data = {
        'depth': depth,
        'northing': northing,
        'easting': easting
    }
    df = pd.DataFrame(data=data)
    df.to_csv(fname)

    return None