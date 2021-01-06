import pytest
import numpy as np
import numpy.testing as npt
from hypothesis import given
from hypothesis import assume
from hypothesis.strategies import floats
from pytest import approx

from . import same_len_lists

from ..geometry import direction_vector
from ..geometry import angle_between
from .. import geometry

@given(floats(allow_nan=False, allow_infinity=False), floats(allow_nan=False, allow_infinity=False))
def test_unit_vector_domain(inc, azi):
    northing, easting, vd = direction_vector(inc, azi)
    assert -1 <= vd <= 1
    assert -1 <= northing <= 1
    assert -1 <= easting <= 1

@given(floats(allow_nan=False, allow_infinity=False))
def test_zero_inc_yields_vertical_nev(azi):
    assert direction_vector(0.0, azi) == (0, 0, 1)

@given(floats(allow_nan=False, allow_infinity=False))
def test_zero_azi_fixes_easting(inc):
    northing, easting, vd = direction_vector(inc, 0.0)
    assert -1 <= vd <= 1
    assert -1 <= northing <= 1
    assert easting == 0

#test up/down and cardinal points
@given(floats(allow_nan=False, allow_infinity=False))
def test_180_inc_yields_vertical_nev(azi):
    assert direction_vector(180., azi) == (approx(0), approx(0), -1)

def test_n_hor_yields_north_nev():
    assert direction_vector(90., 0) == (1, approx(0), approx(0))

def test_s_hor_yields_south_nev():
    assert direction_vector(90., 180.) == (-1, approx(0), approx(0))

def test_e_hor_yields_east_nev():
    assert direction_vector(90., 90.) == (approx(0), 1, approx(0))

def test_w_hor_yields_west_nev():
    assert direction_vector(90., 270.) == (approx(0), -1, approx(0))

# Systematic random orientations covering all eight octants
# we use https://www.wolframalpha.com/ in order to generate
# the corresponding polar coordinates to serve as inputs to
# direction_vector()
# Where the z value is negative, the z-output of wolframalpha
# is negated to match our depth convention

def test_north_east_up():
    #[x  y  z]
    #[0.43, 0.17, 0.93]
    n, e, v = direction_vector(26.436, 21.5713)
    assert n == approx(0.414017, rel=1e-5)
    assert e == approx(0.163681, rel=1e-5)
    assert v == approx(0.895432, rel=1e-5)

def test_north_east_down():
    #[x  y -z]
    #[0.75, 0.87, -0.34]
    n, e, v = direction_vector(73.5113, 49.2364)
    assert n == approx(0.626088, rel=1e-5)
    assert e == approx(0.726262, rel=1e-5)
    assert v == approx(0.283827, rel=1e-5)

def test_south_east_up():
    #[x -y  z]
    #[0.86, -0.34, 0.65]
    n, e, v = direction_vector(54.8975, -21.5713)
    assert n == approx(0.760824, rel=1e-5)
    assert e == approx(-0.300791, rel=1e-5)
    assert v == approx(0.575041, rel=1e-5)

def test_south_east_down():
    #[x -y -z]
    #[0.88, -0.98, -0.97]
    n, e, v = direction_vector(53.63, -48.0775)
    assert n == approx(0.537977, rel=1e-5)
    assert e == approx(-0.599111, rel=1e-5)
    assert v == approx(0.592998, rel=1e-5)

def test_north_west_up():
    #[-x  y  z]
    #[-0.43, 0.54, 0.62]
    n, e, v = direction_vector(48.0707, 128.53)
    assert n == approx(-0.463438, rel=1e-5)
    assert e == approx(0.581993, rel=1e-5)
    assert v == approx(0.668214, rel=1e-5)

def test_north_west_down():
    #[-x  y -z]
    #[-0.87, 0.63, -0.94]
    n, e, v = direction_vector(48.8105, 144.09)
    assert n == approx(-0.60951, rel=1e-5)
    assert e == approx(0.44137, rel=1e-5)
    assert v == approx(0.658551, rel=1e-5)

def test_south_west_up():
    #[-x -y  z]
    #[-0.77, -0.58, 0.84]
    n, e, v = direction_vector(48.9322, -143.011)
    assert n == approx(-0.602206, rel=1e-5)
    assert e == approx(-0.45361, rel=1e-5)
    assert v == approx(0.656952, rel=1e-5)

def test_south_west_down():
    #[-x -y -z]
    #[-0.98, -0.49, -0.64]
    n, e, v = direction_vector(59.7101, -153.435)
    assert n == approx(-0.772324, rel=1e-5)
    assert e == approx(-0.386162, rel=1e-5)
    assert v == approx(0.504375, rel=1e-5)

def test_array():
    n, e, v = direction_vector([59.7101, 48.9322], [-153.435, -143.011])
    np.testing.assert_allclose(n, np.array([-0.772324, -0.602206]), rtol=1e-5)
    np.testing.assert_allclose(e, np.array([-0.386162, -0.45361]), rtol=1e-5)
    np.testing.assert_allclose(v, np.array([0.504375, 0.656952]), rtol=1e-5)

from ..geometry import spherical

@given(
    floats(allow_nan = False),
    floats(allow_nan = False),
    floats(allow_nan = False),
)
def test_spherical_single(n, e, v):
    inc, azi = spherical(n, e, v)
    assert 0 <= azi < 360

@given(same_len_lists())
def test_spherical_list(nev):
    """The same_len_lists can draw values that when squared overflow floats.
    For regular floats, this doesn't flag, but numpy warns on it. It's
    considered a caller problem if the value does overflow.

    TODO
    ----
    Consider either properly warning or consistently failing when a partial
    computation overflows. A solution could be to coerce even regular floats to
    numpy, and look for the warning. For now, do the python thing and just
    carry on.
    """
    n, e, v = nev
    inc, azi = spherical(n, e, v)
    assert np.all(0 <= azi)
    assert np.all(azi < 360)

def normalize(x, y, z):
    magnitude = np.sqrt(x * x + y * y + z * z)
    assume(np.isfinite(magnitude))
    assume(magnitude != 0)
    return x / magnitude, y / magnitude, z / magnitude

@given(
    floats(allow_nan = False, allow_infinity = False, min_value = 1e-12, max_value=1e12),
    floats(allow_nan = False, allow_infinity = False, min_value = 1e-12, max_value=1e12),
    floats(allow_nan = False, allow_infinity = False, min_value = 1e-12, max_value=1e12),
)
def test_spherical_position_roundtrip(n, e, v):
    n, e, v = normalize(n, e, v)

    inc, azi = spherical(n, e, v)
    N, E, V = direction_vector(inc, azi)

    if np.isnan(V):
        assert np.isnan(v)
    else:
        assert V == approx(v, abs = 1e-9)

    if np.isnan(N):
        assert np.isnan(n)
    else:
        assert N == approx(n, abs = 1e-9)

    if np.isnan(E):
        assert np.isnan(e)
    else:
        assert E == approx(e, abs = 1e-9)

def test_angle_between():
    assert angle_between((1, 0, 0), (0, 1, 0))  == approx(1.5707963267948966)
    assert angle_between((1, 0, 0), (1, 0, 0))  == 0.0
    assert angle_between((1, 0, 0), (-1, 0, 0)) == approx(3.141592653589793)

    a = [[1, 0, 0]]
    b = [[0, 1, 0]]
    npt.assert_array_almost_equal(angle_between(a, b), [1.5707963267948966])

def test_normalize():
    a = [2, 4, 3]
    b = [5, 6, 7]

    norma = [0.371391, 0.742781, 0.557086]
    normb = [0.476731, 0.572078, 0.667424]
    npt.assert_array_almost_equal(geometry.normalize(a), norma)
    npt.assert_array_almost_equal(geometry.normalize(b), normb)
    ab = [a, b]
    npt.assert_array_almost_equal(geometry.normalize(ab), [norma, normb])
