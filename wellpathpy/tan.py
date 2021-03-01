import numpy as np

from .checkarrays import checkarrays

def tan_method(md, inc, azi, choice='avg'):
    """Calculate TVD using one of the tangential method.

    Parameters
    ----------
    md : float
        measured depth
    inc : float
        well deviation in degrees
    azi : float
        well azimuth in degrees
    choice : str
        choice of tangential method to run
        one of `['high', 'low', 'avg', 'bal']`

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    """

    if choice == 'bal':
        return balanced_tan(md, inc, azi)

    md, inc, azi = checkarrays(md, inc, azi)

    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]

    if choice == 'high':
        # extract the lower survey stations
        inc = inc_r[1:]
        azi = azi_r[1:]
    elif choice == 'low':
        # extract the upper survey stations
        inc = inc_r[:-1]
        azi = azi_r[:-1]
    elif choice == 'avg':
        inc = (inc_r[1:] + inc_r[:-1]) / 2
        azi = (azi_r[1:] + azi_r[:-1]) / 2
    else:
        msg = 'unknown choice {}, must be one of {}'
        choices = ['high', 'low', 'avg', 'bal']
        raise ValueError(msg.format(choice, ' '.join(choices)))

    northing = np.cumsum((md_lower - md_upper) * np.sin(inc) * np.cos(azi))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md_lower - md_upper) * np.sin(inc) * np.sin(azi))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * np.cos(inc))
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting

def high_tan(md, inc, azi):
    """Calculate TVD using high tangential method.

    This method takes the sines and cosines of the inclination and azimuth
    at the bottom of the survey interval to estimate tvd.

    This method is not recommended as it can make gross tvd and offset
    errors in typical deviated wells.

    Parameters
    ----------
    md : float
        measured depth
    inc : float
        well deviation in degrees
    azi : float
        well azimuth in degrees

    Notes
    -----
    Formulae:

    .. math::
        northing = (md_l - md_u) \cdot sin(inc_l) \cdot cos(azi_l)

    .. math::
        easting = (md_l - md_u) \cdot sin(inc_l) \cdot sin(azi_l)

    .. math::
        tvd = (md_l - md_u) \cdot cos(azi_l)

    where:

    - :math:`md_u`: upper survey station depth MD
    - :math:`md_l`: lower survey station depth MD
    - :math:`inc_l`: lower survey station inclination in degrees
    - :math:`azi_l`: lower survey station azimuth in degrees

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    """
    return tan_method(md, inc, azi, choice='high')

def low_tan(md, inc, azi):
    """Calculate TVD using low tangential method.

    This method takes the sines and cosines of the inclination and azimuth
    at the top of the survey interval to estimate tvd.

    This method is not recommended as it can make gross tvd and offset
    errors in typical deviated wells.

    Parameters
    ----------
    md : float
        measured depth
    inc : float
        well deviation in degrees
    azi : float
        well azimuth in degrees

    Notes
    -----
    Formulae:

    .. math::
        northing = (md_l - md_u) \cdot sin(inc_u) \cdot cos(azi_u)

    .. math::
        easting = (md_l - md_u) \cdot sin(inc_u) \cdot sin(azi_u)

    .. math::
        tvd = (md_l - md_u) \cdot cos(azi_u)

    where:

    - :math:`md_u`: upper survey station depth MD
    - :math:`md_l`: lower survey station depth MD
    - :math:`inc_u`: upper survey station inclination in degrees
    - :math:`azi_u`: upper survey station azimuth in degrees

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    """
    return tan_method(md, inc, azi, choice='low')

def average_tan(md, inc, azi):
    """Calculate TVD using average tangential method.

    This method averages the inclination and azimuth at the top and
    bottom of the survey interval before taking their sine and cosine,
    this average angle is used to estimate tvd.

    Parameters
    ----------
    md : float
        measured depth
    inc : float
        well deviation in degrees
    azi : float
        well azimuth in degrees

    Notes
    -----
    Formulae:

    .. math::
        northing = (md_l - md_u) \cdot sin(\\frac{inc_l + inc_u}{2}) \cdot cos(\\frac{azi_l + azi_u}{2})

    .. math::
        easting = (md_l - md_u) \cdot sin(\\frac{inc_l + inc_u}{2}) \cdot sin(\\frac{azi_l + azi_u}{2})

    .. math::
        tvd = (md_l - md_u) \cdot cos(\\frac{inc_l + inc_u}{2})

    where:

    - :math:`md_u`: upper survey station depth MD
    - :math:`md_l`: lower survey station depth MD
    - :math:`inc_u`: upper survey station inclination in degrees
    - :math:`inc_l`: lower survey station inclination in degrees
    - :math:`azi_u`: upper survey station azimuth in degrees
    - :math:`azi_l`: lower survey station azimuth in degrees

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    """
    return tan_method(md, inc, azi, choice='avg')

def balanced_tan(md, inc, azi):
    """Calculate TVD using balanced tangential method.

    This method takes the sines and cosines of the inclination and azimuth
    at the top and bottom of the survey interval before averaging them,
    this average angle is used to estimate tvd.

    This will provide a smoother curve than the ave_tan method but requires
    closely spaced survey stations to avoid errors.

    Parameters
    ----------
    md : float
        measured depth
    inc : float
        well deviation in degrees
    azi : float
        well azimuth in degrees

    Notes
    -----
    Formulae:

    .. math::
        northing = (md_l - md_u) \cdot \\frac{sin(inc_u) \cdot cos(azi_u) + sin(inc_l) \cdot cos(azi_l)}{2}

    .. math::
        easting = (md_l - md_u) \cdot \\frac{sin(inc_u) \cdot sin(azi_u) + sin(inc_l) \cdot sin(azi_l)}{2}

    .. math::
        tvd = (md_l - md_u) \cdot \\frac{cos(inc_l) + cos(inc_u)}{2}

    where:

    - :math:`md_u`: upper survey station depth MD
    - :math:`md_l`: lower survey station depth MD
    - :math:`inc_u`: upper survey station inclination in degrees
    - :math:`inc_l`: lower survey station inclination in degrees
    - :math:`azi_u`: upper survey station azimuth in degrees
    - :math:`azi_l`: lower survey station azimuth in degrees

    Returns
    -------
    tvd : array_like of float
        true vertical depth
    northing : array_like of float
    easting : array_like of float
    """
    md, inc, azi = checkarrays(md, inc, azi)

    # convert degrees to radians for numpy functions
    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    # extract upper and lower survey stations
    md_upper, md_lower = md[:-1], md[1:]
    inc_upper, inc_lower = inc_r[:-1], inc_r[1:]
    azi_upper, azi_lower = azi_r[:-1], azi_r[1:]

    northing = np.cumsum((md_lower - md_upper) * (np.sin(inc_upper) * np.cos(azi_upper)
                                                  + np.sin(inc_lower) * np.cos(azi_lower)) / 2)
    northing = np.insert(northing, 0, 0)


    easting = np.cumsum((md_lower - md_upper) * (np.sin(inc_upper) * np.sin(azi_upper)
                                                  + np.sin(inc_lower) * np.sin(azi_lower)) / 2)
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md_lower - md_upper) * (np.cos(inc_lower) + np.cos(inc_upper)) / 2)
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting
