import numpy as np

from .checkarrays import checkarrays

def tan_method(md, inc, azi, choice='avg'):
    """
    ToDo
    ----
    Implement surface location
        replace `np.insert([tvd, northing, easting], 0, 0)` with
        `np.insert([tvd, northing, easting], 0, <surface location>)`
    """

    if choice == 'bal':
        return bal_tan_method(md, inc, azi)

    md, inc, azi = checkarrays(md, inc, azi)

    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]

    if choice == 'high':
        # extract the lower survey stations
        inc = inc_r[1:]
        azi = azi_r[1:]
    elif choice == 'low':
        # extract the upper survey stations
        inc = inc_r[:-1]
        azi = azi_r[:-1]
    elif choice == 'avg':
        inc = (inc_r[1:] + inc_r[:-1]) / 2
        azi = (azi_r[1:] + azi_r[:-1]) / 2
    else:
        msg = 'unknown choice {}, must be one of {}'
        choices = ['high', 'low', 'avg', 'bal']
        raise ValueError(msg.format(choice, ' '.join(choices)))

    northing = np.cumsum((md_lower - md_upper) * np.sin(inc) * np.cos(azi))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * np.sin(inc) * np.sin(azi))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * np.cos(inc))
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting

def high_tan_method(md, inc, azi):
    """
    Calculate TVD using high tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the bottom of the survey interval to estimate tvd.

    This method is not recommended as it can make gross tvd and offset
    errors in typical deviated wells.

    Formula
    -------
    northing = sum((md_lower - md_upper) * sin(inc_lower) * cos(azi_lower))
    easting = sum((md_lower - md_upper) * sin(inc_lower) * sin(azi_lower))
    tvd = sum((md_lower - md_upper) * cos(azi_lower))

    where:
    md_upper: upper survey station depth MD
    md_lower: lower survey station depth MD
    inc_lower: lower survey station inclination in degrees
    azi_lower: lower survey station azimuth in degrees

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
    return tan_method(md, inc, azi, choice='high')

def low_tan_method(md, inc, azi):
    """
    Calculate TVD using low tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the top of the survey interval to estimate tvd.

    This method is not recommended as it can make gross tvd and offset
    errors in typical deviated wells.

    Formula
    -------
    northing = sum((md_lower - md_upper) * sin(inc_upper) * cos(azi_upper))
    easting = sum((md_lower - md_upper) * sin(inc_upper) * sin(azi_upper))
    tvd = sum((md_lower - md_upper) * cos(azi_upper))

    where:
    md_upper: upper survey station depth MD
    md_lower: lower survey station depth MD
    inc_upper: upper survey station inclination in degrees
    azi_upper: upper survey station azimuth in degrees

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
    return tan_method(md, inc, azi, choice='low')

def ave_tan_method(md, inc, azi):
    """
    Calculate TVD using average tangential method.
    This method averages the inclination and azimuth at the top and
    bottom of the survey interval before taking their sine and cosine,
    this average angle is used to estimate tvd.

    Formula
    -------
    northing = sum((md_lower - md_upper) * sin((inc_lower + inc_upper) / 2) * cos((azi_lower + azi_upper) / 2))
    easting = sum((md_lower - md_upper) * sin((inc_lower + inc_upper) / 2) * sin((azi_lower + azi_upper) / 2))
    tvd = sum((md_lower - md_upper) * cos((inc_lower + inc_upper) / 2))

    where:
    md_upper: upper survey station depth MD
    md_lower: lower survey station depth MD
    inc_upper: upper survey station inclination in degrees
    inc_lower: lower survey station inclination in degrees
    azi_upper: upper survey station azimuth in degrees
    azi_lower: lower survey station azimuth in degrees

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
    return tan_method(md, inc, azi, choice='avg')

def bal_tan_method(md, inc, azi):
    """
    Calculate TVD using balanced tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the top and bottom of the survey interval before averaging them,
    this average angle is used to estimate tvd.

    This will provide a smoother curve than the ave_tan method but requires
    closely spaced survey stations to avoid errors.

    Formula
    -------
    northing = sum((md_lower - md_upper) * ((sin(inc_upper) * cos(azi_upper) + sin(inc_lower) * cos(azi_lower)) / 2))
    easting = sum((md_lower - md_upper) * ((sin(inc_upper) * sin(azi_upper) + sin(inc_lower) * sin(azi_lower)) / 2))
    tvd = sum((md_lower - md_upper) * (cos(inc_lower) + cos(inc_upper)) / 2))

    where:
    md_upper: upper survey station depth MD
    md_lower: lower survey station depth MD
    inc_upper: upper survey station inclination in degrees
    inc_lower: lower survey station inclination in degrees
    azi_upper: upper survey station azimuth in degrees
    azi_lower: lower survey station azimuth in degrees

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
    inc_upper, inc_lower = inc_r[:-1], inc_r[1:]
    azi_upper, azi_lower = azi_r[:-1], azi_r[1:]

    northing = np.cumsum((md_lower - md_upper) * (np.sin(inc_upper) * np.cos(azi_upper)
                                                  + np.sin(inc_lower) * np.cos(azi_lower)) / 2)
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * (np.sin(inc_upper) * np.sin(azi_upper)
                                                  + np.sin(inc_lower) * np.sin(azi_lower)) / 2)
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * (np.cos(inc_lower) + np.cos(inc_upper)) / 2)
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting
