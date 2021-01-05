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
