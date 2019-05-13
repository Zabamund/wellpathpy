import pytest
import numpy as np

from ..header import get_header

# defaults
def test_defaults():
    v = get_header()
    expected = { 'datum': 'kb', 'units': 'm', 'elevation': 0. }
    assert v == expected

# datum
def test_datum_kb():
    v = get_header(datum='kb')
    expected = 'kb'
    assert v['datum'] == expected

def test_datum_dfe():
    v = get_header(datum='dfe')
    expected = 'dfe'
    assert v['datum'] == expected

def test_datum_rt():
    v = get_header(datum='rt')
    expected = 'rt'
    assert v['datum'] == expected

def test_wrong_datum_throws():
    with pytest.raises(ValueError):
        _ = get_header(datum='kdjfkjdf')

# units
def test_units_m():
    v = get_header(units='m')
    expected = 'm'
    assert v['units'] == expected

def test_units_ft():
    v = get_header(units='ft')
    expected = 'ft'
    assert v['units'] == expected

def test_units_throws():
    with pytest.raises(ValueError):
        _ = get_header(units='adaswesf')

# elevation
def test_elevation_float():
    v = get_header(elevation=0.0)
    expected = 0.0
    assert v['elevation'] == expected

def test_elevation_nan():
    v = get_header(elevation=np.nan)
    assert np.isnan(v['elevation'])

def test_elevation_throws():
    with pytest.raises(TypeError):
        _ = get_header(elevation='0.0')