import pytest
from hypothesis import assume
from hypothesis import given
from hypothesis.strategies import composite
import numpy as np

from . import same_len_lists
from .. import deviation
from .. import position_log

@composite
def deviation_survey(draw):
    dev = draw(same_len_lists(min_value = 0))
    md  = np.unique(dev[0])
    inc = np.mod(dev[1], 90)[:len(md)]
    azi = np.mod(dev[2], 360)[:len(md)]
    assume(len(md) >= 2)
    return md, inc, azi

# This test is marked as expected-to-fail, since fuzzing generates absurd edge
# cases which give reasonably slight inaccuracies. The tolerance could be
# significantly increased, but that would open up for errors passing in silence.
@pytest.mark.xfail(strict = True)
@given(deviation_survey())
def test_resample_onto_unchanged_md(survey):
    md, inc, azi = survey

    dev = deviation(md, inc, azi)
    pos = dev.minimum_curvature()
    resampled = pos.resample(depths = md)

    np.testing.assert_allclose(pos.depth, resampled.depth)
    np.testing.assert_allclose(pos.northing, resampled.northing)
    np.testing.assert_allclose(pos.easting, resampled.easting)

def test_copy():
    original = position_log(np.array([]), np.array([1,2,3,4]), [4,3,2,1], [1,1,1,1])
    copy = original.copy()
    original.depth += 10
    np.testing.assert_equal([1,2,3,4], copy.depth)

def test_straight_down_segment_preserves_depth():
    """
    When the well is straight down, the vertical depth and measured depth
    should increase at the same rate.
    """
    md  = [0, 3, 7]
    inc = [0, 0, 0]
    azi = [0, 0, 0]

    pos = deviation(md, inc, azi).minimum_curvature()
    np.testing.assert_array_equal(md, pos.depth)
    np.testing.assert_array_equal([0, 0, 0], pos.northing)
    np.testing.assert_array_equal([0, 0, 0], pos.easting)

def test_straight_nonvertical_segment():
    """
    The well has a constant inclination which means delta(md) > delta(vd), the
    path is not straight down. This doesn't test for the path going back up.
    """
    md  = np.array([1,  3,  7])
    inc = np.array([30, 30, 30])
    azi = np.array([0, 0, 0])

    pos = deviation(md, inc, azi).minimum_curvature()
    delta_md = md[1:] - md[:-1]
    delta_vd = pos.depth[1:] - pos.depth[:-1]
    assert (delta_md > delta_vd).all()
