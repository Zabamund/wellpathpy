import pytest
import io
import numpy as np

from ..checkarrays import checkarrays, checkarrays_tvd
from ..write import deviation_to_csv, position_to_csv

_md = [0, 1, 2, 3, 4]
_inc = [0, 12, 22, 32, 90]
_azi = [355, 350, 340, 330, 320]
_tvd = [0, 10, 20, 30, 40]
_northing = [100, 200, 300, 400, 500]
_easting = [100, 200, 300, 400, 500]

def test_deviation_not_floats_throws():
    output = io.StringIO()
    md, inc, azi = _md.copy(), _inc.copy(), _azi.copy()
    for val in [md, inc, azi]:
        last = val[-1]
        val[-1] = 'value'
        with pytest.raises(ValueError):
            deviation_to_csv(output, md, inc, azi)
        val[-1] = last

def test_position_not_floats_throws():
    output = io.StringIO()
    tvd, northing, easting = _tvd.copy(), _northing.copy(), _easting.copy()
    for val in [tvd, northing, easting]:
        last = val[-1]
        val[-1]= 'value'
        with pytest.raises(ValueError):
            position_to_csv(output, tvd, northing, easting)
        val[-1] = last

def test_deviation_unequal_shapes_throws():
    output = io.StringIO()
    md, inc, azi = _md.copy(), _inc.copy(), _azi.copy()
    for val in [md, inc, azi]:
        last = val.pop()
        with pytest.raises(ValueError):
            deviation_to_csv(output, md, inc, azi)
        val.append(last)

def test_position_unequal_shapes_throws():
    output = io.StringIO()
    tvd, northing, easting = _tvd.copy(), _northing.copy(), _easting.copy()
    for val in [tvd, northing, easting]:
        last = val.pop()
        with pytest.raises(ValueError):
            position_to_csv(output, tvd, northing, easting)
        val.append(last)

def test_deviation_nan_values_throws():
    output = io.StringIO()
    md, inc, azi = _md.copy(), _inc.copy(), _azi.copy()
    for val in [md, inc, azi]:
        last = val[-1]
        val[-1] = np.nan
        with pytest.raises(ValueError):
            deviation_to_csv(output, md, inc, azi)
        val[-1] = last

def test_position_nan_values_throws():
    output = io.StringIO()
    tvd, northing, easting = _tvd.copy(), _northing.copy(), _easting.copy()
    for val in [tvd, northing, easting]:
        last = val[-1]
        val[-1] = np.nan
        with pytest.raises(ValueError):
            position_to_csv(output, tvd, northing, easting)
        val[-1] = last