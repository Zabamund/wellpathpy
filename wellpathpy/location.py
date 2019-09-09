import numpy as np

from .checkarrays import checkarrays_tvd

def loc_to_wellhead(tvd, northing, easting, surface_northing, surface_easting):
    """Move deviation to wellhead location.

    Adds the surface location coordinates to the northing and easting arrays.

    This method does not check that surface location units are consistent
    with well deviation units, this is the user's responsibility.

    Parameters
    ----------
    tvd : float
        true verical depth
    northing : float
        north-offset from zero reference point
    easting : float
        east-offset from zero reference point

    Notes
    -----
    `northing` and `easting` units should be the same as the input deviation or results will be wrong

    Returns
    -------
    tvd : array_like of float
    northing : array_like of float
    easting : array_like of float
    """

    tvd, northing, easting = checkarrays_tvd(tvd, northing, easting)

    northing += surface_northing
    easting += surface_easting

    return tvd, northing, easting


def loc_to_zero(tvd, northing, easting, surface_northing, surface_easting):
    """Move deviation to zero coordinates.

    Substracts the surface location coordinates from the northing and easting arrays.

    This method does not check that surface location units are consistent
    with well deviation units, this is the user's responsibility.

    Parameters
    ----------
    tvd : float
        true verical depth
    northing : float
        north-offset from zero reference point
    easting : float
        east-offset from zero reference point

    Notes
    -----
    `northing` and `easting` units should be the same as the input deviation or results will be wrong

    Returns
    -------
    tvd : array_like of float
    northing : array_like of float
    easting : array_like of float
    """

    tvd, northing, easting = checkarrays_tvd(tvd, northing, easting)

    northing -= surface_northing
    easting -= surface_easting

    return tvd, northing, easting

def loc_to_tvdss(tvd, northing, easting, datum_elevation):
    """
    Shift tvd to tvdss given datum elevation.

    Parameters
    ----------
    tvd : float
        true verical depth
    northing : float
        north-offset from zero reference point
    easting : float
        east-offset from zero reference point

    Notes
    -----
    `northing` and `easting` units should be the same as the input deviation or results will be wrong

    Substracts the tvd array from the datum elevation:

    - Offshore wells will have negative values of tvdss.
    - Onshore wells will have positive values of tvdss.

    This method does not check that datum elevation units are consistent with well tvd units, this is the user's responsibility.

    Returns
    -------
    tvdss : array_like of float
        true vertical depth subsea
    northing : array_like of float
    easting : array_like of float

    """

    tvd, northing, easting = checkarrays_tvd(tvd, northing, easting)

    tvdss = datum_elevation - tvd

    return tvdss, northing, easting