import numpy as np

def ave_tan_method(md, inc, azi):
    """
    Calculate TVD using average tangential method.
    This method averages the inclination and azimuth at the top and
    bottom of the survey interval before taking their sine and cosine,
    this average angle is used to estimate tvd.

    Parameters
    ----------
    md: float, measured depth in m or ft
    inc: float, well deviation in degrees
    azi: float, well azimuth in degrees

    Returns
    -------
    Deviation converted to TVD, easting, northing
        tvd in m or feet,
        northing in m or feet,
        easting in m or feet

    ToDo
    ----
    Implement surface location
        replace `np.insert([tvd, northing, easting], 0, 0)` with
        `np.insert([tvd, northing, easting], 0, <surface location>)`
    """
    # inputs are array-like
    md = np.asarray(md, dtype = np.float)
    inc = np.asarray(inc, dtype = np.float)
    azi = np.asarray(azi, dtype = np.float)

    # inputs are same shape
    if not (md.shape == inc.shape == azi.shape):
        raise ValueError('md, inc, and azi must be the same shape')

    # md array increases strictly at each step
    try:
        1 / bool(np.all(md[1:] > md[:-1]))
    except ZeroDivisionError:
        raise ZeroDivisionError('md must have strictly increasing values')

    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]
    incl_upper, incl_lower = inc_r[:-1], inc_r[1:]
    azi_upper, azi_lower = azi_r[:-1], azi_r[1:]

    northing = np.cumsum((md_lower - md_upper) * np.sin((incl_lower + incl_upper) / 2)
                         * np.cos((azi_lower + azi_upper) / 2))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * np.sin((incl_lower + incl_upper) / 2)
                        * np.sin((azi_lower + azi_upper) / 2))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * np.cos((incl_lower + incl_upper) / 2))
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting