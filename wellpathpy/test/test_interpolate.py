import pytest
import numpy as np
import pandas as pd
from scipy import interpolate

from ..interpolate import resample_deviation, resample_position

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
        _ = resample_deviation(md=np.array([1,2,np.nan]),
                                inc=np.array([1,2,3]),
                                azi=np.array([1,2,3]),
                                md_step=1)

def test_inter_dev_inc_throws():
    with pytest.raises(ValueError):
        _ = resample_deviation(md=np.array([1,2,3]),
                                inc=np.array([1,2,np.nan]),
                                azi=np.array([1,2,3]),
                                md_step=1)

def test_inter_dev_azi_throws():
    with pytest.raises(ValueError):
        _ = resample_deviation(md=np.array([1,2,3]),
                                inc=np.array([1,2,3]),
                                azi=np.array([1,2,np.nan]),
                                md_step=1)

def test_inter_pos_md_throws():
    with pytest.raises(ValueError):
        _ = resample_position(tvd=np.array([1,2,np.nan]),
                                easting=np.array([1,2,3]),
                                northing=np.array([1,2,3]),
                                tvd_step=1)

def test_inter_pos_inc_throws():
    with pytest.raises(ValueError):
        _ = resample_position(tvd=np.array([1,2,3]),
                                easting=np.array([1,2,np.nan]),
                                northing=np.array([1,2,3]),
                                tvd_step=1)

def test_inter_pos_azi_throws():
    with pytest.raises(ValueError):
        _ = resample_position(tvd=np.array([1,2,3]),
                                easting=np.array([1,2,3]),
                                northing=np.array([1,2,np.nan]),
                                tvd_step=1)

# md_step and tvd_step are of type int
def test_inter_dev_md_step_throws():
    with pytest.raises(TypeError):
        _ = resample_deviation(md=np.array([1,2,3]),
                                inc=np.array([1,2,3]),
                                azi=np.array([1,2,3]),
                                md_step='1')

def test_inter_dev_tvd_step_throws():
    with pytest.raises(TypeError):
        _ = resample_position(tvd=np.array([1,2,3]),
                                easting=np.array([1,2,3]),
                                northing=np.array([1,2,3]),
                                tvd_step='1')

def test_inter_pos_not_monotonic_throws():
    with pytest.raises(ValueError):
        _ = resample_position(tvd=np.array([1,2,4,4,5]),
                                easting=np.array([1,2,3,4,5]),
                                northing=np.array([1,2,3,4,5]),
                                tvd_step=1)
    with pytest.raises(ValueError):
        _ = resample_position(tvd=np.array([1,2,6,4,5]),
                                easting=np.array([1,2,3,4,5]),
                                northing=np.array([1,2,3,4,5]),
                                tvd_step=1)

def euclidean_norm(x, y):
    return np.abs(x - y)

def sample_interval(curve):
    return np.linspace(
        start = curve.min(),
        stop = curve.max(),
        num = int(len(curve) * 1.6),
    )

def test_equivalent_deviation_curve_after_interpolation_md(well):
    steps = [1,2,3,4,5]
    for step in steps:
        md, _, _ = resample_deviation(well.md, well.inc, well.azi, md_step=step)
        assert md[0] == well.md[0]
        assert md[-1] == well.md[-1]
        np.testing.assert_almost_equal(md[1:-1] - md[:-2], step, decimal=1)
    dec_steps = [.1,.2,.3,.4,.5]
    for dec_step in dec_steps:
        md, _, _ = resample_deviation(well.md, well.inc, well.azi, md_step=dec_step)
        assert md[0] == well.md[0]
        assert md[-1] == well.md[-1]
        np.testing.assert_almost_equal(md[1:-1] - md[:-2], dec_step, decimal=2)

def test_equivalent_deviation_curve_after_interpolation_inc(well):
    md, x, _ = resample_deviation(well.md, well.inc, well.azi, md_step=1)
    refmd = sample_interval(md)
    reference = interpolate.interp1d(well.md, well.inc)(refmd)
    result = interpolate.interp1d(md, x)(refmd)
    np.testing.assert_allclose(reference, result, rtol = 1.5)

def test_equivalent_deviation_curve_after_interpolation_azi(well):
    md, _, x = resample_deviation(well.md, well.inc, well.azi, md_step=1)
    refmd = sample_interval(md)
    reference = interpolate.interp1d(well.md, well.azi)(refmd)
    result = interpolate.interp1d(md, x)(refmd)
    np.testing.assert_allclose(reference, result, rtol = 1.5)

def test_equivalent_position_curve_after_interpolation_tvd(well):
    well.tvd = well.tvd[:-40]
    well.easting = well.easting[:-40]
    well.northing = well.northing[:-40]
    steps = [1,2,3,4,5]
    for step in steps:
        tvd, _, _ = resample_position(well.tvd, well.easting, well.northing, tvd_step=step)
        assert tvd[0] == well.tvd[0]
        assert tvd[-1] == well.tvd[-1]
        np.testing.assert_almost_equal(tvd[1:-1] - tvd[:-2], step, decimal=1)
    dec_steps = [.1,.2,.3,.4,.5]
    for dec_step in dec_steps:
        tvd, _, _ = resample_position(well.tvd, well.easting, well.northing, tvd_step=dec_step)
        assert tvd[0] == well.tvd[0]
        assert tvd[-1] == well.tvd[-1]
        np.testing.assert_almost_equal(tvd[1:-1] - tvd[:-2], dec_step, decimal=2)

def test_equivalent_position_curve_after_interpolation_easting(well):
    well.tvd = well.tvd[:-40]
    well.easting = well.easting[:-40]
    well.northing = well.northing[:-40]
    tvd, _, x = resample_position(well.tvd, well.easting, well.northing, tvd_step=1)
    reftvd = sample_interval(tvd)
    reference = interpolate.interp1d(well.tvd, well.easting)(reftvd)
    result = interpolate.interp1d(tvd, x)(reftvd)
    np.testing.assert_allclose(reference, result, rtol = 0.5)

def test_equivalent_position_curve_after_interpolation_northing(well):
    well.tvd = well.tvd[:-40]
    well.easting = well.easting[:-40]
    well.northing = well.northing[:-40]
    tvd, x, _ = resample_position(well.tvd, well.easting, well.northing, tvd_step=1)
    reftvd = sample_interval(tvd)
    reference = interpolate.interp1d(well.tvd, well.northing)(reftvd)
    result = interpolate.interp1d(tvd, x)(reftvd)
    np.testing.assert_allclose(reference, result, rtol = 1)
