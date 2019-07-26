import numpy as np
from scipy import interpolate

from .checkarrays import checkarrays, checkarrays_tvd, checkarrays_monotonic_tvd

def interpolate_deviation(md, inc, azi, md_step=1):
    """
    Interpolate a well deviation to a given step.

    Parameters
    ----------
    md: float, measured depth (units not defined)
    inc: float, well inclination in degrees from vertical
    azi: float, well azimuth in degrees from North
    md_step: int or float, md increment to interpolate to

    Returns
    -------
    Deviation intepolated to new md_step:
        md, inc, azi

    Notes
    -----
    This function should not be used before md->tvd conversion.
    Note that the input arrays must not contain NaN values.

    """

    md, inc, azi = checkarrays(md, inc, azi)

    for input_array in [md, inc, azi]:
        if np.isnan(input_array).any():
            raise ValueError('md, inc and azi cannot contain NaN values.')

    try:
        new_md = np.arange(md.min(), md.max() + md_step, md_step)
        new_md[-1] = md.max()
    except TypeError:
        raise TypeError('md_step must be int or float')

    f_inc = interpolate.interp1d(md, inc)
    new_inc = f_inc(new_md)
    f_azi = interpolate.interp1d(md, azi)
    new_azi = f_azi(new_md)

    return new_md, new_inc, new_azi

def interpolate_position(tvd, easting, northing, tvd_step=1):
    """
    Interpolate a well positional log to a given step.

    Parameters
    ----------
    tvd: float, true verical depth (units not defined)
    northing: float, north-offset from zero reference point
        the units should be the same as the input deviation
        or the results will be wrong
    easting: float, east-offset from zero reference point
        the units should be the same as the input deviation
        or the results will be wrong
    tvd_step: int or float, tvd increment to interpolate to

    Returns
    -------
    Deviation intepolated to new step:
        tvd, easting, northing

    Notes
    -----
    This function should not be used before tvd->md conversion.
    Note that the input arrays must not contain NaN values.
    The tvd values must be strictly increasing, i.e. this
    method will not work on horizontal wells, use
    `interpolate_deviation` for those wells.

    """
    tvd, easting, northing = checkarrays_monotonic_tvd(tvd, easting, northing)

    for input_array in [tvd, northing, easting]:
        if np.isnan(input_array).any():
            raise ValueError('tvd, northing and easting cannot contain NaN values.')

    try:
        new_tvd = np.arange(tvd[0], tvd[-1] + tvd_step, tvd_step)
        new_tvd[-1] = tvd[-1]
    except TypeError:
        raise TypeError('tvd_step must be int or float')

    f_easting = interpolate.interp1d(tvd, easting)
    new_easting = f_easting(new_tvd)
    f_northing = interpolate.interp1d(tvd, northing)
    new_northing = f_northing(new_tvd)

    return new_tvd, new_easting, new_northing