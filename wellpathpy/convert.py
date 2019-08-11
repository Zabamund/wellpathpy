import numpy as np
import pint

def unit_convert(data, src='m', dst='m'):
    """
    Converts data from src units to dst units using pint

    Parameters
    ----------
    data: int, float or np.ndarray
        the data to convert, either a single data point or a numpy array
    src: str
        the source unit: any units in `dir(pint.UnitRegistry())`
    dst: str
        the destination unit: any units in `dir(pint.UnitRegistry())`

    Returns
    -------
    data: float or np.ndarray
        the data converted from src to dst

    """
    ureg = pint.UnitRegistry()

    data = data * ureg(src)

    return data.to(ureg(dst))