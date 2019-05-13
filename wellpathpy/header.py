def get_header(datum='kb', units='m', elevation=0.):
    """
    Record deviation header information needed for depth
    reference calculation into DataFrame.
    
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
        
    return {'datum': datum, 'units': units, 'elevation': elevation}