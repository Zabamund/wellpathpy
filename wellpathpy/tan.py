import numpy as np

from .checkarrays import checkarrays

def tan_method(md, inc, azi, choice = 'high'):
    """
    ToDo
    ----
    Implement surface location
        replace `np.insert([tvd, northing, easting], 0, 0)` with
        `np.insert([tvd, northing, easting], 0, <surface location>)`
    """
    if choice is None:
        choice = 'high'

    md, inc, azi = checkarrays(md, inc, azi)

    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]

    if choice == 'high':
        # extract the upper survey stations
        incl_choice = inc_r[1:]
        azi_choice = azi_r[1:]
    elif choice == 'low':
        # extract the lower survey stations
        incl_choice = inc_r[:-1]
        azi_choice = azi_r[:-1]
    elif choice == 'avg':
        inc_choice = (inc_r[1:] + inc_r[:-1]) / 2
        azi_choice = (azi_r[1:] + azi_r[:-1]) / 2
    else:
        msg = 'unknown choice {}, must be one of {}'
        choices = ['high', 'low', 'avg']
        raise ValueError(msg.format(choice, ' '.join(choices)))

    northing = np.cumsum((md_lower - md_upper) * np.sin(inc_choice) * np.cos(azi_choice))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * np.sin(inc_choice) * np.sin(azi_choice))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * np.cos(inc_choice))
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting

def high_tan_method(md, inc, azi):
    """
    Calculate TVD using high tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the bottom of the survey interval to estimate tvd.

    This method is not recommended as it can make gross tvd and offset
    errors in typical deviated wells.

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
    """
    return tan_method(md, inc, azi, choice = 'high')

def low_tan_method(md, inc, azi):
    """
    Calculate TVD using low tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the top of the survey interval to estimate tvd.

    This method is not recommended as it can make gross tvd and offset
    errors in typical deviated wells.

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
    """
    return tan_method(md, inc, azi, choice = 'low')

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
    """
    return tan_method(md, inc, azi, choice = 'avg')
