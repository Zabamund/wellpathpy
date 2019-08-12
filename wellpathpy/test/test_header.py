import pytest
import numpy as np
import json
import io

from ..header import read_header_json

good_keys = [
    'datum',
    'elevation_units',
    'elevation',
    'surface_coordinates_units',
    'surface_easting',
    'surface_northing'
    ]
good_header = {
    'datum': 'kb',
    'elevation_units': 'm',
    'elevation': 100.0,
    'surface_coordinates_units': 'm',
    'surface_easting': 1000.0,
    'surface_northing': 2000.0
    }

def test_all_keys_present():
    output = io.StringIO()
    json.dump(good_header, output)
    output.seek(0)
    _ = read_header_json(output)

def test_too_many_keys():
    header = good_header.copy()
    header['new_key'] = 100
    output = io.StringIO()
    json.dump(header, output)
    output.seek(0)
    _ = read_header_json(output)

def test_keys_missing():
    for key in good_keys:
        header = good_header.copy()
        header.pop(key)
        output = io.StringIO()
        json.dump(header, output)
        output.seek(0)
        with pytest.raises(ValueError):
            _ = read_header_json(output)

def test_non_floats_raise():
    numeric_values = ['elevation', 'surface_easting', 'surface_northing']
    for num_value in numeric_values:
        header = good_header.copy()
        header[num_value] = 'hundred'
        output = io.StringIO()
        json.dump(header, output)
        output.seek(0)
        with pytest.raises(ValueError):
            _ = read_header_json(output)