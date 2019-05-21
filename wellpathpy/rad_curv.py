import numpy as np

from .checkarrays import checkarrays

def rad_curve_method(md, inc, azi):
    """
    Calculate TVD using radius or curvature method.
    Caution: this will yield unreliable results when data are closely spaced
        or when the borehole is straight but deviated.

    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points.

    Formula
    -------
    northing = sum((md_lower - md_upper) * cos(inc_upper) - cos(inc_lower) * sin(azi_lower) - sin(azi_upper)
                                                        / (inc_lower - inc_upper) * (azi_lower - azi_upper))
    easting = sum((md_lower - md_upper) * cos(inc_upper) - cos(inc_lower) * cos(azi_upper) - cos(azi_lower)
                                                        / (inc_lower - inc_upper) * (azi_lower - azi_upper))
    tvd = sum((md_lower - md_upper) * sin(inc_lower) - sin(inc_upper) / (inc_lower - inc_upper))

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
    incl_upper, incl_lower = inc_r[:-1], inc_r[1:]
    azi_upper, azi_lower = azi_r[:-1], azi_r[1:]

    # fix for delta_inc or delta_azi is zero
    delta_inc = np.where(incl_lower - incl_upper == 0., 0.000001, incl_lower - incl_upper)
    delta_azi = np.where(azi_lower - azi_upper == 0., 0.000001, azi_lower - azi_upper)

    #1: North = SUM (MD2 - MD1) * (Cos WD1 - Cos WD2) * (Sin HAZ2 - Sin HAZ1) / ((WD2 - WD1) * (HAZ2 - HAZ1))
    #2: East = SUM (MD2 - MD1) * (Cos WD1 - Cos WD2) * (Cos HAZ1 - Cos HAZ2) / ((WD2 - WD1) * (HAZ2 - HAZ1)}
    #3: TVD = SUM (MD2 - MD1) * (Sin WD2 - Sin WD1) / (WD2 - WD1)

    northing = np.cumsum((md_lower - md_upper) * (np.cos(incl_upper) - np.cos(incl_lower)) * (np.sin(azi_lower) - np.sin(azi_upper)) / delta_inc * delta_azi)
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * (np.cos(incl_upper) - np.cos(incl_lower)) * (np.cos(azi_upper) - np.cos(azi_lower)) / delta_inc * delta_azi)
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * (np.sin(incl_lower) - np.sin(incl_upper)) / delta_inc)
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting