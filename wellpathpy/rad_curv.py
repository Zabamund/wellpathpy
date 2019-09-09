import numpy as np

from .checkarrays import checkarrays

def radius_curvature(md, inc, azi):
    """Calculate TVD using radius or curvature method.

    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points.

    Parameters
    ----------
    md : float
        measured depth
    inc : float
        well deviation in degrees
    azi : float
        well azimuth in degrees

    Notes
    -----
    Caution:

    this method will yield unreliable results when data are closely spaced or when the borehole is straight but deviated.

    Formulae:

    .. math::
        northing = (md_l - md_u)
                   \cdot cos(inc_u) - cos(inc_l)
                   \cdot \\frac{sin(azi_l) - sin(azi_u)}{(inc_l - inc_u) \cdot (azi_l - azi_u)}

    .. math::
        easting = (md_l - md_u)
                  \cdot cos(inc_u) - cos(inc_l)
                  \cdot \\frac{cos(azi_u) - cos(azi_l)}{(inc_l - inc_u) \cdot (azi_l - azi_u)}


    .. math::
        tvd = (md_l - md_u)
              \cdot \\frac{sin(inc_l) - sin(inc_u)}{(inc_l - inc_u)}

    where:

    - :math:`md_u`: upper survey station depth MD
    - :math:`md_l`: lower survey station depth MD
    - :math:`inc_u`: upper survey station inclination in degrees
    - :math:`inc_l`: lower survey station inclination in degrees
    - :math:`azi_u`: upper survey station azimuth in degrees
    - :math:`azi_l`: lower survey station azimuth in degrees

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    """
    md, inc, azi = checkarrays(md, inc, azi)

    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]
    incl_upper, incl_lower = inc_r[:-1], inc_r[1:]
    azi_upper, azi_lower = azi_r[:-1], azi_r[1:]

    # fix for delta_inc or delta_azi is zero
    delta_inc = np.where(incl_lower - incl_upper == 0., 0.000001, incl_lower - incl_upper)
    delta_azi = np.where(azi_lower - azi_upper == 0., 0.000001, azi_lower - azi_upper)

    northing = np.cumsum((md_lower - md_upper) * (np.cos(incl_upper) - np.cos(incl_lower)) * (np.sin(azi_lower) - np.sin(azi_upper)) / (delta_inc * delta_azi))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * (np.cos(incl_upper) - np.cos(incl_lower)) * (np.cos(azi_upper) - np.cos(azi_lower)) / (delta_inc * delta_azi))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * (np.sin(incl_lower) - np.sin(incl_upper)) / delta_inc)
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting
