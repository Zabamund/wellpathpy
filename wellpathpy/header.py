import json

def read_header_json(fname):
    """Read deviation header

    The deviation header information is needed for surface
    location and tvdss calculation.
    This function loads data from a json file into a dict.

    Parameters
    ----------
    fname : str
        path to a json file
        the json file should have the following format:

        {
        "datum": "kb",
        "elevation_units": "m",
        "elevation": 100.0,
        "surface_coordinates_units": "m",
        "surface_easting": 1000.0,
        "surface_northing": 2000.0
        }

    Notes
    -----
    required keys: datum, elevation_units, elevation, surface_coordinates_units, surface_easting, surface_northing

    datum : str
        kb, dfe or rt

    elevation_units : str

    elevation : float
        datum elevation in elevation_units above mean sea level

    surface_coordinates_units : str

    surface_easting : float
        wellhead surface location in surface_coordinates_units
        east of reference

    surface_northing : float, optional
        wellhead surface location in surface_coordinates_units
        north of reference

    datum is not used in calculation

    Glossary
    --------
    kb (kelly bushing),
    dfe (drill floor elevation),
    rt (rotary table)

    Returns
    -------
    header : dict
    """
    try:
        header = json.load(fname)
    except TypeError: # is a file object already
        with open(str(fname)) as f:
            header = json.load(f)

    good_keys = {
        'datum',
        'elevation_units',
        'elevation',
        'surface_coordinates_units',
        'surface_easting',
        'surface_northing'
    }

    missing_keys = good_keys.difference(header.keys())
    if missing_keys:
        raise ValueError('missing keys: {}'.format(', '.join(missing_keys)))

    numeric_values = ['elevation', 'surface_easting', 'surface_northing']
    for num_value in numeric_values:
        header[num_value] = float(header[num_value])

    return header