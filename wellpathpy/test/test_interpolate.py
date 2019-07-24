import pytest
import numpy as np
import pandas as pd
from scipy import interpolate

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

def sample_interval(curve):
    return np.linspace(
        start = curve.min(),
        stop = curve.max(),
        num = int(len(curve) * 1.6),
    )

def test_equivalent_deviation_curve_after_interpolation_md(well):
    md, _, _ = interpolate_deviation(well.md, well.inc, well.azi, md_step=1)
    assert md[0] == well.md[0]
    assert md[-1] <= well.md[-1]

def test_equivalent_deviation_curve_after_interpolation_inc(well):
    md, x, _ = interpolate_deviation(well.md, well.inc, well.azi, md_step=1)
    refmd = sample_interval(md)
    reference = interpolate.interp1d(well.md, well.inc)(refmd)
    result = interpolate.interp1d(md, x)(refmd)
    np.testing.assert_allclose(reference, result, rtol = 1.5)

def test_equivalent_deviation_curve_after_interpolation_azi(well):
    md, _, x = interpolate_deviation(well.md, well.inc, well.azi, md_step=1)
    refmd = sample_interval(md)
    reference = interpolate.interp1d(well.md, well.azi)(refmd)
    result = interpolate.interp1d(md, x)(refmd)
    np.testing.assert_allclose(reference, result, rtol = 1.5)

def test_equivalent_position_curve_after_interpolation_tvd(well):
    # this assertion is pretty funky, but it's at this stage quite unclear how
    # the md/tvd are supposed to behave.
    #
    # Until a decision is made on how to deal with the end-of-interval values,
    # spacing between samples, configurability and more, it's ok for the
    # assertion to stand out and be weird
    tvd, _, _ = interpolate_position(well.tvd, well.easting, well.northing, tvd_step=1)
    assert tvd[0] == well.tvd[0]

def test_equivalent_position_curve_after_interpolation_easting(well):
    tvd, x, _ = interpolate_position(well.tvd, well.easting, well.northing, tvd_step=1)
    reftvd = sample_interval(tvd)
    reference = interpolate.interp1d(well.tvd, well.easting)(reftvd)
    result = interpolate.interp1d(tvd, x)(reftvd)
    np.testing.assert_allclose(reference, result, rtol = 0.5)

def test_equivalent_position_curve_after_interpolation_northing(well):
    tvd, _, x = interpolate_position(well.tvd, well.easting, well.northing, tvd_step=1)
    reftvd = sample_interval(tvd)
    reference = interpolate.interp1d(well.tvd, well.northing)(reftvd)
    result = interpolate.interp1d(tvd, x)(reftvd)
    np.testing.assert_allclose(reference, result, rtol = 1)
