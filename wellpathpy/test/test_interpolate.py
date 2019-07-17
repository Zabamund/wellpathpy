import pytest
import numpy as np
import pandas as pd
from dtw import dtw

from ..interpolate import interpolate_deviation, interpolate_position

class Chest:
    """A dumb object to just hold member varibles for the fixture
    """
    pass

@pytest.fixture(params = ['9', '10'])
def well(request):
    # The tests should not depend on what file the data is from, because it
    # tests round-trip properties and not specifically the data itself.
    # Instead of writing every test twice, use a parametrised fixture [1]
    #
    # [1] https://docs.pytest.org/en/latest/fixture.html#parametrizing-fixtures
    fname = 'wellpathpy/test/fixtures/well{}.csv'.format(request.param)
    csv = pd.read_csv(fname, sep=',')
    w = Chest()
    w.md         = csv['Measured Depth ( ft )'].values
    w.inc        = csv['Inclination ( deg )'].values
    w.azi        = csv['Azimuth Grid ( deg )'].values
    w.tvd        = csv['TVD ( ft )'].values
    w.northing   = csv['Northing ( m )'].values
    w.easting    = csv['Easting ( m )'].values
    return w

# input arrays contain no NaN values
def test_inter_dev_md_throws():
    with pytest.raises(ValueError):
        _ = interpolate_deviation(md=np.array([1,2,np.nan]),
                                inc=np.array([1,2,3]),
                                azi=np.array([1,2,3]),
                                md_step=1)

def test_inter_dev_inc_throws():
    with pytest.raises(ValueError):
        _ = interpolate_deviation(md=np.array([1,2,3]),
                                inc=np.array([1,2,np.nan]),
                                azi=np.array([1,2,3]),
                                md_step=1)

def test_inter_dev_azi_throws():
    with pytest.raises(ValueError):
        _ = interpolate_deviation(md=np.array([1,2,3]),
                                inc=np.array([1,2,3]),
                                azi=np.array([1,2,np.nan]),
                                md_step=1)

def test_inter_pos_md_throws():
    with pytest.raises(ValueError):
        _ = interpolate_position(tvd=np.array([1,2,np.nan]),
                                easting=np.array([1,2,3]),
                                northing=np.array([1,2,3]),
                                tvd_step=1)

def test_inter_pos_inc_throws():
    with pytest.raises(ValueError):
        _ = interpolate_position(tvd=np.array([1,2,3]),
                                easting=np.array([1,2,np.nan]),
                                northing=np.array([1,2,3]),
                                tvd_step=1)

def test_inter_pos_azi_throws():
    with pytest.raises(ValueError):
        _ = interpolate_position(tvd=np.array([1,2,3]),
                                easting=np.array([1,2,3]),
                                northing=np.array([1,2,np.nan]),
                                tvd_step=1)

# md_step and tvd_step are of type int
def test_inter_dev_md_step_throws():
    with pytest.raises(TypeError):
        _ = interpolate_deviation(md=np.array([1,2,3]),
                                inc=np.array([1,2,3]),
                                azi=np.array([1,2,3]),
                                md_step='1')

def test_inter_dev_tvd_step_throws():
    with pytest.raises(TypeError):
        _ = interpolate_position(tvd=np.array([1,2,3]),
                                easting=np.array([1,2,3]),
                                northing=np.array([1,2,3]),
                                tvd_step='1')

def euclidean_norm(x, y):
    return np.abs(x - y)

def test_equivalent_deviation_curve_after_interpolation_md(well):
    y = well.md.reshape(-1,1)
    x, _, _ = interpolate_deviation(well.md, well.inc, well.azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=22)

def test_equivalent_deviation_curve_after_interpolation_inc(well):
    y = well.inc.reshape(-1,1)
    md, x, _ = interpolate_deviation(well.md, well.inc, well.azi, md_step=1)
    distance, *_ = dtw(y, y, dist = euclidean_norm)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=1)

def test_equivalent_deviation_curve_after_interpolation_azi(well):
    y = well.azi.reshape(-1,1)
    _, _, x = interpolate_deviation(well.md, well.inc, well.azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=2)

def test_equivalent_position_curve_after_interpolation_tvd(well):
    y = well.tvd.reshape(-1,1)
    x, _, _ = interpolate_position(well.tvd, well.easting, well.northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=18)

def test_equivalent_position_curve_after_interpolation_easting(well):
    y = well.easting.reshape(-1,1)
    _, x, _ = interpolate_position(well.tvd, well.easting, well.northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=4)

def test_equivalent_position_curve_after_interpolation_northing(well):
    y = well.northing.reshape(-1,1)
    _, _, x = interpolate_position(well.tvd, well.easting, well.northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=2)
