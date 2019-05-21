import numpy as np

from .checkarrays import checkarrays

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
    md, inc, azi = checkarrays(md, inc, azi)

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


    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]
    incl_upper, incl_lower = inc_r[:-1], inc_r[1:]
    azi_upper, azi_lower = azi_r[:-1], azi_r[1:]

    # calculate dogleg
    dl = np.rad2deg(np.arccos(np.cos(incl_lower - incl_upper) -
                              (np.sin(incl_upper) * np.sin(incl_lower) *
                               (1 - np.cos(azi_lower - azi_upper)))))
    dls = (dl * (norm / (md_lower - md_upper)))
    dls = np.insert(dls, 0, 0)

    # ratio factor, correct for dl == 0 values
    rf = 2 / np.deg2rad(dl) * np.tan(np.deg2rad(dl)/2)
    rf = np.where(dl == 0., 1, rf)

    northing = np.cumsum((md_lower - md_upper) / 2 * (np.sin(incl_upper) * np.cos(azi_upper)
                                            + np.sin(incl_lower) * np.cos(azi_lower)) * rf)
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) / 2 * (np.sin(incl_upper) * np.sin(azi_upper)
                                            + np.sin(incl_lower) * np.sin(azi_lower)) * rf)
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) / 2 * (np.cos(incl_upper) + np.cos(incl_lower)) * rf)
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting, dls