import numpy as np

def tangent(inc, azi):
    """ Compute a direction vector from inclination and azimuth

    Convert spherical coordinates (inc, azi) to cubic coordinates (vertical
    depth, northing, easting), a unit length direction vector in a right handed
    coordinate system.

    Parameters
    ----------
    inc : array_like of float
        inclination
    azi : array_like of float
        azimuth

    Returns
    -------
    vd : array_like of float
        vertial direction
    northing : array_like of float
    easting : array_like of float
    """
    inc = np.deg2rad(inc)
    az = np.deg2rad(azi)

    vd = np.cos(inc)
    northing = np.sin(inc) * np.cos(az)
    easting  = np.sin(inc) * np.sin(az)

    return vd, northing, easting
