import pytest
from hypothesis import given
from hypothesis.strategies import floats

from ..geometry import tangent

@given(floats(allow_nan=False, allow_infinity=False), floats(allow_nan=False, allow_infinity=False))
def test_unit_vector_domain(inc, azi):
    vd, northing, easting = tangent(inc, azi)
    assert -1 <= vd <= 1
    assert -1 <= northing <= 1
    assert -1 <= easting <= 1

@given(floats(allow_nan=False, allow_infinity=False))
def test_zero_inc_yields_vertical_nev(azi):
    assert tangent(0.0, azi) == (1, 0, 0)

@given(floats(allow_nan=False, allow_infinity=False))
def test_zero_azi_fixes_easting(inc):
    vd, northing, easting = tangent(inc, 0.0)
    assert -1 <= vd <= 1
    assert -1 <= northing <= 1
    assert easting == 0