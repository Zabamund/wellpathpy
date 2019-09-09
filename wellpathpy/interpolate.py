import numpy as np
from scipy import interpolate

from .checkarrays import checkarrays, checkarrays_tvd, checkarrays_monotonic_tvd

def resample_deviation(md, inc, azi, md_step=1):
    """Resample a well deviation to a given step.

    Parameters
    ----------
    md : float
        measured depth
    inc : float
        well inclination in degrees from vertical
    azi : float
        well azimuth in degrees from North
    md_step : int or float
        md increment to interpolate to

    Notes
    -----
    This function should not be used before md->tvd conversion.
    
    The input arrays must not contain NaN values.

    Returns
    -------
    md : array_like of float
    inc : array_like of float
    azi : array_like of float
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

def resample_position(tvd, easting, northing, tvd_step=1):
    """
    Resample a well positional log to a given step.

    Parameters
    ----------
    tvd : float
        true verical depth
    northing : float
        north-offset from zero reference point
    easting : float
        east-offset from zero reference point
    tvd_step : int or float
        tvd increment to resample to

    Notes
    -----
    This function should not be used before tvd->md conversion.

    The input arrays must not contain NaN values.

    The tvd values must be strictly increasing, i.e. this
    method will not work on horizontal wells, use
    `resample_deviation` for those wells.

    The units should be the same as the input deviation or the results will be wrong.

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
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

    return new_tvd, new_northing, new_easting