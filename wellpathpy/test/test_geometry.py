import pytest
from hypothesis import given
from hypothesis.strategies import floats
from pytest import approx

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

@given(floats(allow_nan=False, allow_infinity=False))
def test_180_inc_yields_vertical_nev(azi):
    assert tangent(180., azi) == (-1, approx(0), approx(0))

def test_n_hor_yields_north_nev():
    assert tangent(90., 0) == (approx(0), 1, approx(0))

def test_s_hor_yields_south_nev():
    assert tangent(90., 180.) == (approx(0), -1, approx(0))

def test_e_hor_yields_east_nev():
    assert tangent(90., 90.) == (approx(0), approx(0), 1)

def test_w_hor_yields_west_nev():
    assert tangent(90., 270.) == (approx(0), approx(0), -1)
