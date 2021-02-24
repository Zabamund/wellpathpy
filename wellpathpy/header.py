import json

def read_header_json(fname):
    """Read deviation header

    The deviation header information is needed for surface
    location and true vertical depth subsea calculations.
    This function loads data from a JSON file into a dict.

    Parameters
    ----------
    fname : str
        JSON object or path to a JSON file

    Notes
    -----
    required keys: elevation_units, elevation, surface_coordinates_units, surface_easting, surface_northing

    optional key: datum

    datum : str
        kb, dfe or rt. datum is not used in calculation

        kb (kelly bushing), dfe (drill floor elevation), rt (rotary table)

    elevation_units : str
        datum elevation units

    elevation : float
        datum elevation in elevation_units above mean sea level

    surface_coordinates_units : str
        surface coordinate units of wellhead

    surface_easting : float
        wellhead surface location in surface_coordinates_units east of reference

    surface_northing : float
        wellhead surface location in surface_coordinates_units north of reference

    Returns
    -------
    header : dict
    """
    try:
        header = json.load(fname)
    except AttributeError: # is a file object already
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