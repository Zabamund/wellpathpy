import numpy as np

from .checkarrays import checkarrays

def high_tan_method(md, inc, azi):
    """
    Calculate TVD using high tangential method.

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
    md, inc, azi = checkarrays(md, inc, azi)

    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]
    incl_lower = inc_r[1:]
    azi_lower = azi_r[1:]

    northing = np.cumsum((md_lower - md_upper) * np.sin(incl_lower) * np.cos(azi_lower))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * np.sin(incl_lower) * np.sin(azi_lower))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * np.cos(incl_lower))
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting