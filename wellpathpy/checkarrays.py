import numpy as np

def checkarrays(md, inc, azi):
    """
    Assure basic preconditions are met, and convert input (md, inc, azi) to
    numpy arrays.

    This function will ensure that:

    - All inputs are convertible to arrays-of-floats, and perform this
      conversion
    - All inputs are of the same shape
    - md is strictly increasing

    Parameters
    ----------
    md: array_like of float
        measured depth
    inc: array_like of float
        well deviation
    azi: array_like of float
        azimuth

    Returns
    -------
    md: array_like of float
        measured depth
    inc: array_like of float
        well deviation
    azi: array_like of float
        azimuth

    Raises
    ------
    ValueError
        If md, inc, or azi, are of different shapes
        If the md values are not strictly increasing
    """
    md = np.asarray(md, dtype = np.float)
    inc = np.asarray(inc, dtype = np.float)
    azi = np.asarray(azi, dtype = np.float)

    if not (md.shape == inc.shape == azi.shape):
        raise ValueError('md, inc, and azi must be the same shape')

    if not np.all(md[1:] > md[:-1]):
        raise ValueError('md must have strictly increasing values')

    return md, inc, azi

def checkarrays_tvd(tvd, northing, easting):
    """
    Assure basic preconditions are met, and convert input (tvd, northing, easting) to
    numpy arrays.

    This function will ensure that:

    - All inputs are convertible to arrays-of-floats, and perform this
      conversion
    - All inputs are of the same shape

    Parameters
    ----------
    tvd: array_like of float
        true vertical depth
    northing: array_like of float
        north-offset
    easting: array_like of float
        east-offset

    Returns
    -------
    tvd: array_like of float
        true vertical depth
    northing: array_like of float
        north-offset
    easting: array_like of float
        east-offset

    Raises
    ------
    ValueError
        If tvd, northing, or easting, are of different shapes
    """
    tvd = np.asarray(tvd, dtype = np.float)
    northing = np.asarray(northing, dtype = np.float)
    easting = np.asarray(easting, dtype = np.float)

    if not (tvd.shape == northing.shape == easting.shape):
        raise ValueError('tvd, northing, and easting must be the same shape')

    return tvd, northing, easting

def checkarrays_monotonic_tvd(tvd, northing, easting):
    """
    Assure basic preconditions are met, and convert input (tvd, northing, easting) to
    numpy arrays.

    This function will ensure that:

    - All inputs are convertible to arrays-of-floats, and perform this
      conversion
    - All inputs are of the same shape
    - tvd is strictly increasing

    Parameters
    ----------
    tvd: array_like of float
        true vertical depth
    northing: array_like of float
        north-offset
    easting: array_like of float
        east-offset

    Returns
    -------
    tvd: array_like of float
        true vertical depth
    northing: array_like of float
        north-offset
    easting: array_like of float
        east-offset

    Raises
    ------
    ValueError
        If tvd, northing, or easting, are of different shapes
        If the tvd values are not strictly increasing
    """
    tvd = np.asarray(tvd, dtype = np.float)
    northing = np.asarray(northing, dtype = np.float)
    easting = np.asarray(easting, dtype = np.float)

    if not (tvd.shape == northing.shape == easting.shape):
        raise ValueError('tvd, northing, and easting must be the same shape')
    if not np.all(tvd[1:] > tvd[:-1]):
        raise ValueError('tvd must have strictly increasing values')

    return tvd, northing, easting