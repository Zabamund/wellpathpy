import numpy as np

from .checkarrays import checkarrays

def minimum_curvature_inner(md, inc, azi):
    """Calculate TVD, northing, easting, and dogleg, using the minimum curvature
    method.

    This is the inner workhorse of the minimum_curvature, and only implement the
    pure mathematics. As a user, you should probably use the minimum_curvature
    function.

    This function considers md unitless, and assumes inc and azi are in radians.

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
    northing : array_like of float
    easting : array_like of float
    dogleg : array_like of float

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
    with np.errstate(divide = 'ignore', invalid = 'ignore'):
        rf = 2 / dogleg * np.tan(dogleg / 2)
        rf = np.where(dogleg == 0., 1, rf)

    md_diff = md_lower - md_upper

    upper = np.sin(inc_upper) * np.cos(azi_upper)
    lower = np.sin(inc_lower) * np.cos(azi_lower)
    northing = np.cumsum((md_diff / 2) * (upper + lower) * rf)

    upper = np.sin(inc_upper) * np.sin(azi_upper)
    lower = np.sin(inc_lower) * np.sin(azi_lower)
    easting = np.cumsum((md_diff / 2) * (upper + lower) * rf)

    tvd = np.cumsum((md_diff / 2) * (np.cos(inc_upper) + np.cos(inc_lower)) * rf)

    return tvd, northing, easting, dogleg

def minimum_curvature(md, inc, azi, course_length=30):
    """Calculate TVD using minimum curvature method.

    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points. This curve is
    smoothed by use of the ratio factor defined by the tortuosity or dogleg
    of the wellpath.

    Parameters
    ----------
    md : float
        measured depth in m or ft
    inc : float
        well deviation in degrees
    azi : float
        well azimuth in degrees
    course_length : float
        dogleg normalisation value, if passed will override md_units

    Notes
    -----
    Formulae:

    .. math::
        dls = arccos[
                  cos(inc_l - inc_u)
                - sin(inc_u) \cdot sin(inc_l) \cdot (1 - cos(azi_l - azi_u))
                ]

    .. math::
        rf = \\frac{2}{dls} \cdot tan(\\frac{dls}{2})

    .. math::
        northing = \\frac{md_l - md_u}{2}
                   \cdot [sin(inc_u)cos(azi_u) + sin(inc_l)cos(azi_l)]
                   \cdot rf

    .. math::
        easting = \\frac{md_l - md_u}{2}
                  \cdot [sin(inc_u)sin(azi_u) + sin(inc_l)sin(azi_l)]
                  \cdot rf

    .. math::
        tvd = \\frac{md_l - md_u}{2}
              \cdot [cos(inc_l) + cos(inc_u)]
              \cdot rf

    where:

    - :math:`dls` : dog leg severity (degrees)
    - :math:`rf` : ratio factor (radians)
    - :math:`md_u` : upper survey station depth MD
    - :math:`md_l` : lower survey station depth MD
    - :math:`inc_u` : upper survey station inclination in degrees
    - :math:`inc_l` : lower survey station inclination in degrees
    - :math:`azi_u` : upper survey station azimuth in degrees
    - :math:`azi_l` : lower survey station azimuth in degrees

    course_length is set to 30 by default, assuming that md units are in meters.
    The user must change course_length if md units are feet.

    Typical course_length values are:

    - m : course_length = 30
    - ft : course_length = 100

    Other values can be passed, but they are non-standard and therefore not
    explicitely supported.

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    dls : array_like of float
        dog leg severity
    """

    try:
        course_length + 0
    except TypeError:
        raise TypeError('course_length must be a float')

    md, inc, azi = checkarrays(md, inc, azi)
    inc = np.deg2rad(inc)
    azi = np.deg2rad(azi)

    md_diff = md[1:] - md[:-1]
    tvd, northing, easting, dogleg = minimum_curvature_inner(md, inc, azi)

    tvd = np.insert(tvd, 0, 0)
    northing = np.insert(northing, 0, 0)
    easting = np.insert(easting, 0, 0)

    dl = np.rad2deg(dogleg)
    dls = dl * (course_length / md_diff)
    dls = np.insert(dls, 0, 0)

    return tvd, northing, easting, dls
