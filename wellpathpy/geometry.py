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

def normalize(v):
    """Normalize vector or compute unit vector

    Compute the normalized (unit vector) [1]_ of v, a vector with the same
    direction, but a length of 1.

    Parameters
    ----------
    v : array_like

    Returns
    -------
    V : array_like
        normalized v

    Notes
    -----
    Normalize is in addition to zeros also sensitive to *very* small floats.

        Falsifying example: deviation_survey=(
            md = array([0.0000000e+000, 1.0000000e+000, 4.1242594e-162]),
            inc = array([0., 0., 0.]),
            azi = array([0., 0., 0.]))

    yields a dot product of 1.0712553822854385, which is outside [-1, 1]. This
    should *really* only show up in testing scenarios and not real data.

    Whenever norm values are less than eps, consider them zero. All zero norms
    are assigned 1, to avoid divide-by-zero. The value for zero is chosen
    arbitrarily as a something that shouldn't happen in real data, or when it
    does is reasonable to consier as zero.

    References
    ----------
    .. [1] https://mathworld.wolfram.com/NormalizedVector.html
    """
    norm = np.atleast_1d(np.linalg.norm(v))
    zero = 1e-15
    norm[np.abs(norm) < zero] = 1.0
    return v / norm

def unit_vector(v):
    """Alias to normalize

    See also
    --------
    normalize
    """
    return normalize(v)

def angle_between(v1, v2):
    """Angle between vectors

    Parameters
    ----------
    v1 : array_like
    v2 : array_like

    Returns
    -------
    alpha : float
        Angle between vectors in radians

    Examples
    --------
    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    v1unit = normalize(v1)
    v2unit = normalize(v2)
    dot = np.dot(v1unit, v2unit)
    # arccos is only defined [-1,1], dot can _sometimes_ go outside this domain
    # because of floating points
    return np.arccos(np.clip(dot, -1.0, 1.0))

def normal_vector(v1, v2):
    """Normal vector to plane given by vectors v1 and v2

    From mathworld [1]_: The normal vector, often simply called the "normal,"
    to a surface is a vector which is perpendicular to the surface at a given
    point.

    Parameters
    ----------
    v1 : array_like
    v2 : array_like

    Returns
    -------
    normal : array_like
        A normal vector to the plane

    References
    ----------
    .. [1] https://mathworld.wolfram.com/NormalVector.html
    """
    return np.cross(v1, v2)
