from hypothesis import assume
from hypothesis import given
from hypothesis.strategies import composite
import numpy as np

from . import same_len_lists
from .. import deviation

@composite
def deviation_survey(draw):
    dev = draw(same_len_lists(min_value = 0))
    md  = np.unique(dev[0])
    inc = np.mod(dev[1], 90)[:len(md)]
    azi = np.mod(dev[2], 360)[:len(md)]
    assume(len(md) >= 2)
    return md, inc, azi

@given(deviation_survey())
def test_resample_onto_unchanged_md(survey):
    md, inc, azi = survey

    dev = deviation(md, inc, azi)
    pos = dev.minimum_curvature()
    resampled = pos.resample(depths = md)

    np.testing.assert_allclose(pos.tvd, resampled.tvd)
    np.testing.assert_allclose(pos.northing, resampled.northing)
    np.testing.assert_allclose(pos.easting, resampled.easting)
