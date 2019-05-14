import numpy as np

def min_curve_method(md, inc, azi):
    """
    Calculate TVD using minimum curvature method.
    
    Parameters
    ----------
    md: float, measured depth in m or ft
    inc: float, well deviation in degrees
    azi: float, well azimuth in degrees
                
    Returns
    -------
    Deviation converted to TVD, easting, northing
        TVD in m or feet,
        northing in m or feet,
        easting in m or feet
    Dogleg
        Dogleg angle in degrees
        
    ToDo
    ----
    Implement DLS
        Dogleg in degrees/100ft or degrees/30m
        Requires `.get_header()` ouput
    """
    # inputs are array-like
    try:
        md = np.array(md) + 0
    except TypeError:
        raise TypeError('md must be array-like')

    try:
        inc = np.array(inc) + 0
    except TypeError:
        raise TypeError('inc must be array-like')

    try:
        azi = np.array(azi) + 0
    except TypeError:
        raise TypeError('azi must be array-like')

    # inputs are same length
    try:
        1 / (md.shape == inc.shape == azi.shape)
    except ZeroDivisionError:
        raise ZeroDivisionError('md, incl and azi must be of same length')

    # inputs dtype are int or float
    try:
        md += 0
    except TypeError:
        raise TypeError('md array must of dtype int or float')

    try:
        inc += 0
    except TypeError:
        raise TypeError('inc array must of dtype int or float')

    try:
        azi += 0
    except TypeError:
        raise TypeError('azi array must of dtype int or float')

    # md array increases strictly at each step
    try:
        1 / bool(np.all(md[1:] > md[:-1]))
    except ZeroDivisionError:
        raise ZeroDivisionError('md must have strictly increasing values')

    # get units
    #norm = 100 if units == 'm' else 30
        
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
    
    # calculate dls
    #dls = (dl * (norm / md_lower - md_upper))
    
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

    return tvd, northing, easting