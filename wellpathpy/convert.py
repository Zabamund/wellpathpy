import numpy as np
import pint

def unit_convert(data, src='m', dst='m', ureg=None):
    """Converts data from src units to dst units using pint

    Parameters
    ----------
    data : int, float or np.ndarray
        the data to convert, either a single data point or a numpy array
    src : str
        the source unit: any units in `dir(pint.UnitRegistry())`
    dst : str
        the destination unit: any units in `dir(pint.UnitRegistry())`
    ureg : pint.registry.UnitRegistry()
        an instance of the Class pint.registry.UnitRegistry()

    Notes
    -----
    ureg
        If none is passed, the default unit registry will be used.

    Examples
    --------
    Convert units with a custom registry:

    >>> import pint
    >>> ureg = pint.UnitRegistry()
    >>> ureg.define('ell = 0.6275 * meter = ell')
    >>> result = unit_convert(data, src='ell', dst='m', ureg=ureg)

    Returns
    -------
    data : float or np.ndarray
    """

    if ureg is None:
        ureg = pint.UnitRegistry()

    data = data * ureg(src)

    return data.to(ureg(dst)).magnitude