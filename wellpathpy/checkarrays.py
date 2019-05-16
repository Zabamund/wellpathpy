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
