import pytest
import numpy as np
import pandas as pd
from dtw import dtw

from ..interpolate import interpolate_deviation, interpolate_position

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


# interpolation is close to input data

# import test well data
well9 = pd.read_csv('./wellpathpy/test/fixtures/well9.csv', sep=",")
well10 = pd.read_csv('./wellpathpy/test/fixtures/well10.csv', sep=",")

# get data series
well9_true_md = well9['Measured Depth ( ft )'].values
well9_true_inc = well9['Inclination ( deg )'].values
well9_true_azi = well9['Azimuth Grid ( deg )'].values
well9_true_tvd = well9['TVD ( ft )'].values
well9_true_northing = well9['Northing ( m )'].values
well9_true_easting = well9['Easting ( m )'].values

well10_true_md = well10['Measured Depth ( ft )'].values
well10_true_inc = well10['Inclination ( deg )'].values
well10_true_azi = well10['Azimuth Grid ( deg )'].values
well10_true_tvd = well10['TVD ( ft )'].values
well10_true_northing = well10['Northing ( m )'].values
well10_true_easting = well10['Easting ( m )'].values

def euclidean_norm(x, y):
    return np.abs(x - y)

def test_w9_dev_md():
    y = well9_true_md.reshape(-1,1)
    x, _, _ = interpolate_deviation(well9_true_md, well9_true_inc, well9_true_azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=20)

def test_w9_dev_inc():
    y = well9_true_inc.reshape(-1,1)
    _, x, _ = interpolate_deviation(well9_true_md, well9_true_inc, well9_true_azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=1)

def test_w9_dev_azi():
    y = well9_true_azi.reshape(-1,1)
    _, _, x = interpolate_deviation(well9_true_md, well9_true_inc, well9_true_azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=2)

def test_w9_pos_tvd():
    y = well9_true_tvd.reshape(-1,1)
    x, _, _ = interpolate_position(well9_true_tvd, well9_true_easting, well9_true_northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=16)

def test_w9_pos_easting():
    y = well9_true_easting.reshape(-1,1)
    _, x, _ = interpolate_position(well9_true_tvd, well9_true_easting, well9_true_northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=2)

def test_w9_pos_northing():
    y = well9_true_northing.reshape(-1,1)
    _, _, x = interpolate_position(well9_true_tvd, well9_true_easting, well9_true_northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=2)

def test_w10_dev_md():
    y = well10_true_md.reshape(-1,1)
    x, _, _ = interpolate_deviation(well10_true_md, well10_true_inc, well10_true_azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=22)

def test_w10_dev_inc():
    y = well10_true_inc.reshape(-1,1)
    _, x, _ = interpolate_deviation(well10_true_md, well10_true_inc, well10_true_azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=1)

def test_w10_dev_azi():
    y = well10_true_azi.reshape(-1,1)
    _, _, x = interpolate_deviation(well10_true_md, well10_true_inc, well10_true_azi, md_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=2)

def test_w10_pos_tvd():
    y = well10_true_tvd.reshape(-1,1)
    x, _, _ = interpolate_position(well10_true_tvd, well10_true_easting, well10_true_northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=20)

def test_w10_pos_easting():
    y = well10_true_easting.reshape(-1,1)
    _, x, _ = interpolate_position(well10_true_tvd, well10_true_easting, well10_true_northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=4)

def test_w10_pos_northing():
    y = well10_true_northing.reshape(-1,1)
    _, _, x = interpolate_position(well10_true_tvd, well10_true_easting, well10_true_northing, tvd_step=1)
    x = x.reshape(-1,1)
    distance, _, _, _ = dtw(x, y, dist=euclidean_norm)
    np.testing.assert_allclose(distance, 0, atol=2)