def get_header(datum='kb', units='m', elevation=0., surface_easting=0., surface_northing=0.):
    """
    Record deviation header information needed for depth
    reference calculation into dict.

    Parameters
    ----------
    datum: str, default 'kb', {'kb', 'dfe', 'rt'}
        'kb' (kellybushing),
        'dfe' (drill floor elevation),
        'rt' (rotary table)
    units: str, default 'm', {'m', 'ft'}
        'm' (metres),
        'ft' (feet)
    elevation: float, default 0.,
        <datum> <elevation> in <units>
        above mean sea level
    surface_easting: float, default 0.,
        wellhead surface location in m east of reference
    surface_northing: float, default 0.,
        wellhead surface location in m north of reference

    Returns
    -------
    dict
        deviation header dictionnary
    """

    if datum not in {'kb', 'dfe', 'rt'}:
        raise ValueError('datum must be kb, dfe or rt')

    if units not in {'m', 'ft'}:
        raise ValueError('units must be m or ft')

    try:
        elevation = float(elevation + 0)
    except TypeError:
        raise TypeError('elevation must be float')

    try:
        surface_easting = float(surface_easting + 0)
    except TypeError:
        raise TypeError('surface_easting must be a float')

    try:
        surface_northing = float(surface_northing + 0)
    except TypeError:
        raise TypeError('surface_northing must be a float')

    return {'datum': datum,
            'units': units,
            'elevation': elevation,
            'surface_easting': surface_easting,
            'surface_northing': surface_northing,
            }