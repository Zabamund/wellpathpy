import numpy as np

from .checkarrays import checkarrays

def minimum_curvature(md, inc, azi):
    """Minimum curvature

    Calculate TVD, northing, easting, and dogleg, using the minimum curvature
    method.

    This is the inner workhorse of the min_curve_method, and only implement the
    pure mathematics. As a user, you should probably use the min_curve_method
    function.

    This function considers md unitless, and assumes inc and azi are in
    radians.

    Parameters
    ----------
    md : array_like of float
        measured depth
    inc : array_like of float
        inclination in radians
    azi : array_like of float
        azimuth in radians

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    dogleg : array_like of float

    Notes
    -----
    This function does not insert surface location
    """
    md, inc, azi = checkarrays(md, inc, azi)


    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]
    inc_upper, inc_lower = inc[:-1], inc[1:]
    azi_upper, azi_lower = azi[:-1], azi[1:]

    cos_inc = np.cos(inc_lower - inc_upper)
    sin_inc = np.sin(inc_upper) * np.sin(inc_lower)
    cos_azi = 1 - np.cos(azi_lower - azi_upper)

    dogleg = np.arccos(cos_inc - (sin_inc * cos_azi))

    # ratio factor, correct for dogleg == 0 values
    rf = 2 / dogleg * np.tan(dogleg / 2)
    rf = np.where(dogleg == 0., 1, rf)

    md_diff = md_lower - md_upper

    upper = np.sin(inc_upper) * np.cos(azi_upper)
    lower = np.sin(inc_lower) * np.cos(azi_lower) * rf
    northing = np.cumsum(md_diff / 2 * (upper + lower))

    upper = np.sin(inc_upper) * np.sin(azi_upper)
    lower = np.sin(inc_lower) * np.sin(azi_lower) * rf
    easting = np.cumsum(md_diff / 2 * (upper + lower))

    tvd = np.cumsum(md_diff / 2 * (np.cos(inc_upper) + np.cos(inc_lower)) * rf)

    return tvd, northing, easting, dogleg

def min_curve_method(md, inc, azi, md_units='m', norm_opt=0):
    """
    Calculate TVD using minimum curvature method.

    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points. This curve is
    smoothed by use of the ratio factor defined by the tortuosity or dogleg
    of the wellpath.

    Formula
    -------
    dls = arccos(cos(inc_lower - inc_upper) - sin(inc_upper) * sin(inc_lower) * (1 - cos(azi_lower - azi_upper)))
    rf = 2 / dls * (tan(dls/2))
    northing = sum((md_lower - md_upper) * (sin(inc_upper) * cos(azi_upper) + sin(inc_lower) * cos(azi_lower) / 2) * cf)
    easting = sum((md_lower - md_upper) *(sin(inc_upper) * sin(azi_upper) + sin(inc_lower) * sin(azi_lower) / 2) * cf)
    tvd = sum((md_lower - md_upper) * (cos(inc_lower) + cos(inc_upper) / 2) * cf)

    where:
    dls: dog leg severity (degrees)
    rf: ratio factor (radians)
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
    md_units: str, measured depth units in m or ft
        used for dogleg severity calculation
    norm_opt: float, dogleg normalisation value,
        if passed will override md_units

    Returns
    -------
    Deviation converted to TVD, easting, northing
        tvd in m or feet,
        northing in m or feet,
        easting in m or feet
    Dogleg severity
        dls: dogleg severity angle in degrees per normalisation value
            (normalisation value is deg/100ft, deg/30m or deg/<norm_opt>)

    ToDo
    ----
    Implement surface location
        replace `np.insert([tvd, northing, easting], 0, 0)` with
        `np.insert([tvd, northing, easting], 0, <surface location>)`
    """

    # get units and normalising for dls
    try:
        norm_opt + 0
    except TypeError:
        raise TypeError('norm_opt must be a float')

    if norm_opt != 0:
        norm = norm_opt
    else:
        if md_units == 'm':
            norm = 30
        elif md_units == 'ft':
            norm = 100
        else:
            raise ValueError('md_units must be either m or ft')

    md, inc, azi = checkarrays(md, inc, azi)
    inc = np.deg2rad(inc)
    azi = np.deg2rad(azi)

    md_diff = md[1:] - md[:-1]
    tvd, northing, easting, dogleg = minimum_curvature(md, inc, azi)

    # TODO: replace with surface location which may be non-zero
    tvd = np.insert(tvd, 0, 0)
    northing = np.insert(northing, 0, 0)
    easting = np.insert(easting, 0, 0)

    # calculate dogleg severity
    dl = np.rad2deg(dogleg)
    dls = dl * (norm / md_diff)
    dls = np.insert(dls, 0, 0)

    return tvd, northing, easting, dls
