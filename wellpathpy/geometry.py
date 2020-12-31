import numpy as np

def direction_vector(inc, azi):
    """ Compute a direction vector from inclination and azimuth

    Convert spherical coordinates (inc, azi) to cubic coordinates (vertical
    depth, northing, easting), a unit length direction vector in a right handed
    coordinate system.

    Parameters
    ----------
    inc : array_like of float
        inclination in degrees
    azi : array_like of float
        azimuth in degrees

    Returns
    -------
    northing : array_like of float
    easting : array_like of float
    vd : array_like of float
        vertial direction

    Examples
    --------
    Inverse of spherical:
    >>> inc, azi = spherical(N1, E1, V1)
    >>> N2, E2, V2 = direction_vector(inc, azi)
    >>> N1 == N2
    True
    >>> E1 == E2
    True
    >>> V1 == V2
    True
    >>> inc2, azi2 = spherical(N, E, V)

    """
    inc = np.deg2rad(inc)
    az = np.deg2rad(azi)

    vd = np.cos(inc)
    northing = np.sin(inc) * np.cos(az)
    easting  = np.sin(inc) * np.sin(az)

    return northing, easting, vd

def spherical(northing, easting, depth):
    """[N E V] -> (inc, azi)

    Convert a unit vector [N E V] to spherical coordinates (inc, azi).

    This function work both on both arrays and single floats.

    https://www.cpp.edu/~ajm/materials/delsph.pdf

    Parameters
    ----------
    northing : array_like of float or float
    easting : array_like of float or float
    depth : array_like of float or float

    Returns
    -------
    inc : array_like of float or float
        inclination in degrees
    azi : array_like of float or float
        azimuth in degrees, [0, 360)

    Notes
    -----
    This functions assumes northing/easting/depth are normalized.

    Examples
    --------
    Inverse of direction_vector:
    >>> N, E, V = direction_vector(inc1, azi)
    >>> inc2, azi2 = spherical(N, E, V)
    >>> inc1 == inc2
    True
    >>> azi1 == azi2
    True

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

