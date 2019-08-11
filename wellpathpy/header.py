import json

def read_header_json(fname):
    """
    Read deviation header information needed for depth
    reference calculation from *.json file into dict.

    Parameters
    ----------
    fname: str, path to a json file with this format:
        {
        "datum": "kb",
        "elevation_units": "m",
        "elevation": 100.0,
        "surface_coordinates_units": "m",
        "surface_easting": 1000.0,
        "surface_northing": 2000.0
        }

    datum: str, usually one of 'kb', 'dfe', 'rt'
        Not used in calculation
        'kb' (kelly bushing),
        'dfe' (drill floor elevation),
        'rt' (rotary table)
    elevation_units: str, for example 'm' or 'ft'
        'm' (metres),
        'ft' (feet)
    elevation: float,
        datum elevation in units above mean sea level
    surface_coordinates_units: str, for example 'm', 'ft'
        'm' (metres),
        'ft' (feet)
    surface_easting: float,
        wellhead surface location in <units> east of reference
    surface_northing: float, default 0.,
        wellhead surface location in <units> north of reference

    Returns
    -------
    dict
        deviation header dictionnary
    """
    try:
        header = json.load(fname)
    except TypeError: # is a file object  already
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