import pytest
from hypothesis import given
from hypothesis.strategies import floats
from pytest import approx
import numpy as np

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

#test up/down and cardinal points
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

# Systematic random orientations covering all eight octants
# we use https://www.wolframalpha.com/ in order to generate
# the corresponding polar coordinates to serve as inputs to
# tangent()
# Where the z value is negative, the z-output of wolframalpha
# is negated to match our depth convention

def test_north_east_up():
    #[x  y  z]
    #[0.43, 0.17, 0.93]
    vd, n, e = tangent(26.436, 21.5713)
    assert n == approx(0.414017, rel=1e-5)
    assert e == approx(0.163681, rel=1e-5)
    assert vd == approx(0.895432, rel=1e-5)

def test_north_east_down():
    #[x  y -z]
    #[0.75, 0.87, -0.34]
    vd, n, e = tangent(73.5113, 49.2364)
    assert n == approx(0.626088, rel=1e-5)
    assert e == approx(0.726262, rel=1e-5)
    assert vd == approx(0.283827, rel=1e-5)

def test_south_east_up():
    #[x -y  z]
    #[0.86, -0.34, 0.65]
    vd, n, e = tangent(54.8975, -21.5713)
    assert n == approx(0.760824, rel=1e-5)
    assert e == approx(-0.300791, rel=1e-5)
    assert vd == approx(0.575041, rel=1e-5)

def test_south_east_down():
    #[x -y -z]
    #[0.88, -0.98, -0.97]
    vd, n, e = tangent(53.63, -48.0775)
    assert n == approx(0.537977, rel=1e-5)
    assert e == approx(-0.599111, rel=1e-5)
    assert vd == approx(0.592998, rel=1e-5)

def test_north_west_up():
    #[-x  y  z]
    #[-0.43, 0.54, 0.62]
    vd, n, e = tangent(48.0707, 128.53)
    assert n == approx(-0.463438, rel=1e-5)
    assert e == approx(0.581993, rel=1e-5)
    assert vd == approx(0.668214, rel=1e-5)

def test_north_west_down():
    #[-x  y -z]
    #[-0.87, 0.63, -0.94]
    vd, n, e = tangent(48.8105, 144.09)
    assert n == approx(-0.60951, rel=1e-5)
    assert e == approx(0.44137, rel=1e-5)
    assert vd == approx(0.658551, rel=1e-5)

def test_south_west_up():
    #[-x -y  z]
    #[-0.77, -0.58, 0.84]
    vd, n, e = tangent(48.9322, -143.011)
    assert n == approx(-0.602206, rel=1e-5)
    assert e == approx(-0.45361, rel=1e-5)
    assert vd == approx(0.656952, rel=1e-5)

def test_south_west_down():
    #[-x -y -z]
    #[-0.98, -0.49, -0.64]
    vd, n, e = tangent(59.7101, -153.435)
    assert n == approx(-0.772324, rel=1e-5)
    assert e == approx(-0.386162, rel=1e-5)
    assert vd == approx(0.504375, rel=1e-5)

def test_array():
    vd, n, e = tangent([59.7101, 48.9322], [-153.435, -143.011])
    np.testing.assert_allclose(n, np.array([-0.772324, -0.602206]), rtol=1e-5)
    np.testing.assert_allclose(e, np.array([-0.386162, -0.45361]), rtol=1e-5)
    np.testing.assert_allclose(vd, np.array([0.504375, 0.656952]), rtol=1e-5)