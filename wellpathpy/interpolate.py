import numpy as np
from scipy import interpolate

from .checkarrays import checkarrays, checkarrays_tvd, checkarrays_monotonic_tvd
from .arc2chord import toUnitDir, toSpherical

def resample_position(tvd, easting, northing, tvd_step=1):
    """
    Resample a well positional log to a given step.

    Parameters
    ----------
    tvd: float, true vertical depth (units not defined)
    northing: float, north-offset from zero reference point
        the units should be the same as the input deviation
        or the results will be wrong
    easting: float, east-offset from zero reference point
        the units should be the same as the input deviation
        or the results will be wrong
    tvd_step: int or float, tvd increment to resample to

    Returns
    -------
    Deviation resampled to new step:
        tvd, easting, northing

    Notes
    -----
    This function should not be used before tvd->md conversion.
    Note that the input arrays must not contain NaN values.
    The tvd values must be strictly increasing, i.e. this
    method will not work on horizontal wells, use
    `resample_deviation` for those wells.

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

def resample_balanced_tangential(md, inc, azi, md_step=1):
    """
    Resample a wellbore path developed using a balanced tangential model to a given depth step.

    Parameters
    ----------
    md: float, measured depth (units not defined)
    inc: float, well inclination in degrees from vertical
    azi: float, well azimuth in degrees from North
    md_step: int or float, md increment to interpolate to

    Returns
    -------
    Deviation resampled to new md_step:
        md, inc, azi, tvd, easting, northing
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
    
    half_lens = (md[1:] - md[:-1]) / 2.0 # get the half the course length between survey stations
    half_mds = np.cumsum(np.repeat(half_lens, 2)) # now repeat every other one to recover total wellbore length
    tangents = toUnitDir(inc, azi) # the unit tangent directions of the wellbore at the survey station

    idx = np.repeat(np.arange(len(tangents)), 2) # [0,1,2] => [0,0,1,1,2,2] - index of tangents including half course positions
    bt_half_rela_pos = half_lens[idx[:-2]] * tangents[idx[1:-1]] # the relative positions including half positions
    bt_half_pos_log = np.cumsum(bt_half_rela_pos, axis=0) # sum the relative postions to absolute

    # interpolate each axis seperately
    f_northing = interpolate.interp1d(half_mds, bt_half_pos_log[:,0])
    new_northing = f_northing(new_md)
    f_easting = interpolate.interp1d(half_mds, bt_half_pos_log[:,1])
    new_easting = f_easting(new_md)
    f_vertical = interpolate.interp1d(half_mds, bt_half_pos_log[:,2])
    new_vertical = f_vertical(new_md)

    t_idx = (np.searchsorted(half_mds, new_md) - 1) # find the indexes of the tangents for each half course
    t_idx[0] = 0 # fixup the first one; it is always 0
    new_inc, new_azi = toSpherical((tangents[idx])[t_idx]) # recover the inc and azi at each new_md

    return new_md, new_inc, new_azi, new_vertical, new_northing, new_easting