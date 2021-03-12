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
    - There are no NaN values in the data

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
        If NaN values are included in md, inc or azi
    """
    md = np.asarray(md, dtype = np.float)
    inc = np.asarray(inc, dtype = np.float)
    azi = np.asarray(azi, dtype = np.float)

    for prop, arr in {'md': md, 'inc': inc, 'azi': azi}.items():
        if np.isnan(arr).any():
            raise ValueError('{} cannot contain nan values'.format(prop))

    if not ((0 <= inc) & (inc < 180)).all():
        raise ValueError('all inc values must be in range 0 <= inc < 180')

    if not ((0 <= azi) & (azi < 360)).all():
        raise ValueError('all azi values must be in range 0 <= azi < 360')

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
    - There are no NaN values in the data

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
        If NaN values are included in tvd, easting or northing
    """
    tvd = np.asarray(tvd, dtype = np.float)
    northing = np.asarray(northing, dtype = np.float)
    easting = np.asarray(easting, dtype = np.float)

    for prop, arr in {'tvd': tvd, 'northing': northing, 'easting': easting}.items():
        if np.isnan(arr).any():
            raise ValueError('{} cannot contain nan values'.format(prop))

    if not (tvd.shape == northing.shape == easting.shape):
        raise ValueError('tvd, northing, and easting must be the same shape')

    return tvd, northing, easting
