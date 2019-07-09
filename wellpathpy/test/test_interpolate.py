import pytest
import numpy as np

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
