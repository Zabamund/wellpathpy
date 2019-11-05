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

def spherical(northing, easting, depth):
    """[N E V] -> (inc, azi)

    Convert a unit vector [N E V] to spherical coordinates (inc, azi).

    This function work both on both arrays and single floats.

    https://www.cpp.edu/~ajm/materials/delsph.pdf

    Parameters
    ----------
    northing : array_like of float or float
        northing in radians
    easting : array_like of float or float
        eastin gin radians
    depth : array_ike of float or float

    Returns
    -------
    inc : array_like of float or float
        inclination in degrees
    azi : array_like of float or float
        azimuth in degrees, [0, 360)
    """
    n2 = northing * northing
    e2 = easting * easting
    inc = np.arctan2(np.sqrt(n2 + e2), depth)
    azi = np.arctan2(easting, northing)

    # for very small, negative angles, angle + 2pi = 2pi, which is outside the
    # output domain [0, 360). this unintuitive approach sorts that out
    twopi = 2.0 * np.pi
    try:
        _ = len(azi)
        azi[azi < 0] += twopi
        azi = np.mod(azi, twopi)
    except TypeError:
        if azi < 0:
            azi += twopi
            azi = np.mod(azi, twopi)

    inc = np.rad2deg(inc)
    azi = np.rad2deg(azi)
    return inc, azi

