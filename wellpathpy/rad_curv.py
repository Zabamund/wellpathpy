import numpy as np

from .checkarrays import checkarrays

def rad_curve_method(md, inc, azi):
    """
    Calculate TVD using radius or curvature method.
    Caution: this will yield unreliable results when data are closely spaced
        or when the borehole is straight but deviated.

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
    incl_upper, incl_lower = inc_r[:-1], inc_r[1:]
    azi_upper, azi_lower = azi_r[:-1], azi_r[1:]

    northing = np.cumsum((md_lower - md_upper) * (np.cos(incl_upper) - np.cos(incl_lower)
                                                  / ((incl_lower - incl_upper) * (azi_lower - azi_upper))))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * (np.cos(incl_upper) - np.cos(incl_lower))
                        * (np.cos(azi_upper) - np.cos(azi_lower))
                        / ((incl_lower - incl_upper) * (azi_lower - azi_upper)))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * (np.sin(incl_lower) - np.sin(incl_upper)) / (incl_lower - incl_upper))
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting