import numpy as np

from .checkarrays import checkarrays, checkarrays_tvd

def deviation_to_csv(fname, md, inc, azi, fmt='%.3f', delimiter=',', header='md,inc,azi', **kwargs):
    """Write a log to a comma-separated values (csv) file.

    Parameters
    ----------
    fname : str or file handle
        file path or object the CSV will be written to.
    md : array-like,
        measured depth
    inc : array-like,
        inclination from vertical
    azi : array-like,
        azimuth from north
    fmt : str
        this is the fmt argument to numpy.savetxt, see:
        https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
    delimiter : str
        String or character separating columns.
    header : str
        String that will be written at the beginning of the file.
        Beware if changing the header that it does not change the order in
        which the data are written, which remains: `md`,`inc`,`azi`.

    Other Parameters
    ----------------
    **kwargs : All other keyword arguments are passed to `np.savetxt`

    Notes
    -----
    This function is totally unit unaware, the user is responsible
    to handle units, for example with the unit_convert function.

    Caution: deviation_to_csv uses Python write mode set to the default: ‘w’
    therefore existing files will be overwritten.
    """

    md, inc, azi = checkarrays(md, inc, azi)

    a = np.asarray([md, inc, azi])
    np.savetxt(fname, a, fmt=fmt, delimiter=delimiter, header=header, **kwargs)

    return None

def position_to_csv(fname, depth, northing, easting, fmt='%.3f', delimiter=',', header='easting,northing,depth', **kwargs):
    """Write a log to a comma-separated values (csv) file.

    Parameters
    ----------
    fname : str or file handle
        file path or object the CSV will be written to.
    depth : array-like,
        true vertical depth (tvd) or
        true vertical depth subsea (tvdss)
    northing : array-like,
        distance north of reference point
    easting : array-like,
        distance east of reference point,
    fmt : str
        this is the fmt argument to numpy.savetxt, see:
        https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
    delimiter : str
        String or character separating columns.
    header : str
        String that will be written at the beginning of the file.
        Beware if changing the header that it does not change the order in
        which the data are written, which remains: `easting`,`northing`,`depth`.

    Other Parameters
    ----------------
    **kwargs : All other keyword arguments are passed to `np.savetxt`

    Notes
    -----
    This function is totally unit unaware, the user is responsible
    to handle units, for example with the unit_convert function.

    Caution: position_to_csv uses Python write mode set to the default: ‘w’
    therefore existing files will be overwritten.
    """

    depth, northing, easting = checkarrays_tvd(depth, northing, easting)

    a = np.asarray([easting, northing, depth])
    np.savetxt(fname, a, fmt=fmt, delimiter=delimiter, header=header, **kwargs)

    return None