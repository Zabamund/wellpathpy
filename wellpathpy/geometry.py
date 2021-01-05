import numpy as np

def direction_vector(inc, azi):
    """(inc, azi) -> [N E V]

    Compute a direction vector from inclination and azimuth.

    Convert spherical coordinates (inc, azi) to cubic coordinates (northing,
    easting, vertical depth), a unit length direction vector in a right handed
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
    v : array_like or array_like of vectors

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

    Examples
    --------
    >>> a = [2, 4, 3]
    >>> b = [5, 6, 7]
    >>> normalize(a)
    [0.371391, 0.742781, 0.557086]
    >>> normalize([a, b])
    [[0.37139068 0.74278135 0.55708601]
     [0.47673129 0.57207755 0.66742381]]
    """
    v = np.asarray(v)
    norm = np.atleast_1d(np.linalg.norm(v, axis = v.ndim - 1))

    zero = 1e-15
    norm.ravel()[np.abs(norm.ravel()) < zero] = 1.0

    if v.ndim == 1:
        return v / norm[:]
    else:
        return v / norm[:, np.newaxis]

def unit_vector(v):
    """Alias to normalize

    See also
    --------
    normalize
    """
    return normalize(v)

def angle_between(v1, v2):
    """Return the angle between (arrays of) vectors

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
    >>> a = [[1, 0, 0]]
    >>> b = [[0, 1, 0]]
    >>> angle_between(a, b)
    [1.5707963267948966]
    """
    # The angle between vectors is computed from the dot-product, but we want
    # to also do this for arrays-of-vectors, and np.dot() interprets that as
    # matrix multiplication.
    v1 = normalize(v1)
    v2 = normalize(v2)
    if v1.ndim == 1:
        dot = np.dot(v1, v2)
    else:
        # This is just a way of writing dot(v1,v2) for an array-of-vectors
        dot = np.einsum('ij,ij->i', v1, v2)

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

def mul_quat(q1, q2):
    """Quaternion multiplication

    This is for internal use and may be removed without notice.
    """
    q3 = np.copy(q1)
    q3[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
    q3[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
    q3[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
    q3[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
    return q3

def rotate(vector, axis, angle):
    """Rotate vector around an axis

    Rotate the vector around the axis.

    Parameters
    ----------
    vector : array_like
        Vector to rotate
    axis : array_like
        Axis to rotate around
    angle : float
        Angle to rotate, in radians

    Returns
    -------
    v : array_like
        The rotated vector
    """
    # Vector rotate is implemented in terms of quaternions - while this means
    # some extra maths, it avoids a heavy scipy dependency for this one
    # operation.
    #
    # In early development, the rotate() function looked like this:
    #     def rotate(vector, axis, angle):
    #         import scipy
    #         from scipy.spatial.transform import Rotation
    #         rot = Rotation.from_rotvec(angle * normalize(axis))
    #         return normalize(rot.apply(normalize(vector)))
    #
    # this is obviously much nicer, but has the drawback of pulling the massive
    # scipy dependency. If wellpathpy should at some point depend on scipy
    # anyway, the implementation of rotate() should be changed to using
    # scipy.spatial.transform.
    #
    # The implementation is short enough to do by hand, and to not pull in a
    # large quaternion library (at which point we might as well pull scipy
    # which is more likely to already be installed).
    #
    # Both implementations are based on answers in this thread, with some
    # slight modifications
    # https://stackoverflow.com/questions/6802577/rotation-of-3d-vector/25709323

    # https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Using_quaternion_as_rotations
    # compute the rotation quaternion
    axis = normalize(axis)
    rotq = np.append([np.cos(angle/2)], np.sin(angle/2) * axis)

    # compute the quaternion form of the vector
    vect = np.append([0], vector)
    vecq = normalize(vect)
    norm = np.linalg.norm(vect)
    # conjugate the rotation quaternion
    conj = np.append(rotq[0], -rotq[1:])
    # multiply with the norm in order to preserve length. As of now the only
    # property used post-rotation is the direction (to compute angles), but
    # preserving vector magnitude means that the numerical values of vectors
    # should be reasonably close, which in turn should make floating-point
    # arithmetic more predictable.
    # r = p' = qpq^-1
    r = mul_quat(rotq, mul_quat(vecq, conj)) * norm
    return r[1:]
