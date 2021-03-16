import pytest
import numpy as np

import hypothesis

from ..tan import tan_method
from ..mincurve import minimum_curvature
from ..rad_curv import radius_curvature
from ..location import loc_to_wellhead
from ..position_log import deviation, position_log as mc

# import test well data
well9 = np.loadtxt('./wellpathpy/test/fixtures/well9.csv', delimiter=",", skiprows=1)
well10 = np.loadtxt('./wellpathpy/test/fixtures/well10.csv', delimiter=",", skiprows=1)
# get data series
well9_true_md_m = well9[:,0] * 0.3048 # converting feet to meters
well9_true_inc = well9[:,1]
well9_true_azi = well9[:,2]
well9_true_tvd_m = well9[:,3] * 0.3048 # converting feet to meters
well9_true_northing = well9[:,5]
well9_true_easting = well9[:,6]
well9_true_dls = well9[:,4]
well9_true_surface_northing = 39998.454
well9_true_surface_easting = 655701.278
well9_true_datum_elevation = 100 * 0.3048 # converting feet to meters

well10_true_md_m = well10[:,0] * 0.3048 # converting feet to meters
well10_true_inc = well10[:,1]
well10_true_azi = well10[:,2]
well10_true_tvd_m = well10[:,3] * 0.3048 # converting feet to meters
well10_true_northing = well10[:,5]
well10_true_easting = well10[:,6]
well10_true_dls = well10[:,4]
well10_true_surface_northing = 40004.564
well10_true_surface_easting = 655701.377
well10_true_datum_elevation = 100 * 0.3048 # converting feet to meters

# test methods
def test_high_tan():
    tvd9, mN9, mE9 = tan_method(well9_true_md_m, well9_true_inc, well9_true_azi, choice='high')
    tvd10, mN10, mE10 = tan_method(well10_true_md_m, well10_true_inc, well10_true_azi, choice='high')
    tvd9, mN9, mE9 = loc_to_wellhead(tvd9, mN9, mE9, 39998.454, 655701.278)
    tvd10, mN10, mE10 = loc_to_wellhead(tvd10, mN10, mE10, 40004.564, 655701.377)
    np.testing.assert_allclose(tvd9, well9_true_tvd_m, atol=12)
    np.testing.assert_allclose(mE9, well9_true_easting, atol=12)
    np.testing.assert_allclose(mN9, well9_true_northing, atol=12)
    np.testing.assert_allclose(tvd10, well10_true_tvd_m, atol=12)
    np.testing.assert_allclose(mE10, well10_true_easting, atol=15)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=12)

def test_low_tan():
    tvd9, mN9, mE9 = tan_method(well9_true_md_m, well9_true_inc, well9_true_azi, choice='low')
    tvd10, mN10, mE10 = tan_method(well10_true_md_m, well10_true_inc, well10_true_azi, choice='low')
    tvd9, mN9, mE9 = loc_to_wellhead(tvd9, mN9, mE9, 39998.454, 655701.278)
    tvd10, mN10, mE10 = loc_to_wellhead(tvd10, mN10, mE10, 40004.564, 655701.377)
    np.testing.assert_allclose(tvd9, well9_true_tvd_m, atol=12)
    np.testing.assert_allclose(mE9, well9_true_easting, atol=12)
    np.testing.assert_allclose(mN9, well9_true_northing, atol=12)
    np.testing.assert_allclose(tvd10, well10_true_tvd_m, atol=12)
    np.testing.assert_allclose(mE10, well10_true_easting, atol=15)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=12)

def test_avg_tan():
    tvd9, mN9, mE9 = tan_method(well9_true_md_m, well9_true_inc, well9_true_azi, choice='avg')
    tvd10, mN10, mE10 = tan_method(well10_true_md_m, well10_true_inc, well10_true_azi, choice='avg')
    tvd9, mN9, mE9 = loc_to_wellhead(tvd9, mN9, mE9, 39998.454, 655701.278)
    tvd10, mN10, mE10 = loc_to_wellhead(tvd10, mN10, mE10, 40004.564, 655701.377)
    np.testing.assert_allclose(tvd9, well9_true_tvd_m, atol=10)
    np.testing.assert_allclose(mE9, well9_true_easting, atol=10)
    np.testing.assert_allclose(mN9, well9_true_northing, atol=10)
    np.testing.assert_allclose(tvd10, well10_true_tvd_m, atol=10)
    np.testing.assert_allclose(mE10, well10_true_easting, atol=10)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=10)

def test_bal_tan():
    tvd9, mN9, mE9 = tan_method(well9_true_md_m, well9_true_inc, well9_true_azi, choice='bal')
    tvd10, mN10, mE10 = tan_method(well10_true_md_m, well10_true_inc, well10_true_azi, choice='bal')
    tvd9, mN9, mE9 = loc_to_wellhead(tvd9, mN9, mE9, 39998.454, 655701.278)
    tvd10, mN10, mE10 = loc_to_wellhead(tvd10, mN10, mE10, 40004.564, 655701.377)
    np.testing.assert_allclose(tvd9, well9_true_tvd_m, atol=10)
    np.testing.assert_allclose(mE9, well9_true_easting, atol=10)
    np.testing.assert_allclose(mN9, well9_true_northing, atol=10)
    np.testing.assert_allclose(tvd10, well10_true_tvd_m, atol=10)
    np.testing.assert_allclose(mE10, well10_true_easting, atol=10)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=10)

def test_min_curve():
    tvd9, mN9, mE9, dls9 = minimum_curvature(well9_true_md_m, well9_true_inc, well9_true_azi)
    tvd10, mN10, mE10, dls10 = minimum_curvature(well10_true_md_m, well10_true_inc, well10_true_azi)
    tvd9, mN9, mE9 = loc_to_wellhead(tvd9, mN9, mE9, 39998.454, 655701.278)
    tvd10, mN10, mE10 = loc_to_wellhead(tvd10, mN10, mE10, 40004.564, 655701.377)
    np.testing.assert_allclose(tvd9, well9_true_tvd_m)
    np.testing.assert_allclose(mE9, well9_true_easting, atol=0.5)
    np.testing.assert_allclose(mN9, well9_true_northing, atol=0.5)
    np.testing.assert_allclose(dls9, well9_true_dls, atol=1)
    np.testing.assert_allclose(tvd10, well10_true_tvd_m)
    np.testing.assert_allclose(mE10, well10_true_easting, atol=0.5)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=0.5)
    np.testing.assert_allclose(dls10, well10_true_dls, atol=1)

def test_min_curve_rf():
    """
    This test was added as the code for mininum curvature initially read:

    ```
    upper = np.sin(inc_upper) * np.cos(azi_upper)
    lower = np.sin(inc_lower) * np.cos(azi_lower) * rf
    northing = np.cumsum(md_diff / 2 * (upper + lower))

    upper = np.sin(inc_upper) * np.sin(azi_upper)
    lower = np.sin(inc_lower) * np.sin(azi_lower) * rf
    easting = np.cumsum(md_diff / 2 * (upper + lower))
    ```

    This was incorrect but not detected because the results were within noise because the angles are small,
    so we use large angles here to force an error with that initial code.

    With the correct code:
    ```
    upper = np.sin(inc_upper) * np.cos(azi_upper)
    lower = np.sin(inc_lower) * np.cos(azi_lower)
    northing = np.cumsum((md_diff / 2) * (upper + lower) * rf)

    upper = np.sin(inc_upper) * np.sin(azi_upper)
    lower = np.sin(inc_lower) * np.sin(azi_lower)
    easting = np.cumsum((md_diff / 2) * (upper + lower) * rf)
    ```
    rf is multiplied to both upper and lower

    the rf synthetic output is stored output from running the function and only serves as a regression test
    """

    md = np.array([10, 20, 30, 40, 50])
    inc = np.array([10, 35, 55, 75, 90])
    azi = np.array([45, 45, 45, 45, 45])

    tvd_ref = np.array([0, 9.16568053, 16.20090348, 20.4056626, 21.70720016])
    mE_ref = np.array([0, 2.68456567, 7.65921952, 14.03529686, 21.02586714])
    mN_ref = np.array([0, 2.68456567, 7.65921952, 14.03529686, 21.02586714])
    dls_ref = np.array([0., 75., 60., 60., 45.])

    tvd, mN, mE, dls = minimum_curvature(md, inc, azi)
    np.testing.assert_allclose(tvd, tvd_ref)
    np.testing.assert_allclose(mN, mN_ref)
    np.testing.assert_allclose(mE, mE_ref)
    np.testing.assert_allclose(dls, dls_ref)

def test_rad_curve():
    tvd9, mN9, mE9 = radius_curvature(well9_true_md_m, well9_true_inc, well9_true_azi)
    tvd10, mN10, mE10 = radius_curvature(well10_true_md_m, well10_true_inc, well10_true_azi)
    tvd9, mN9, mE9 = loc_to_wellhead(tvd9, mN9, mE9, 39998.454, 655701.278)
    tvd10, mN10, mE10 = loc_to_wellhead(tvd10, mN10, mE10, 40004.564, 655701.377)
    np.testing.assert_allclose(tvd9, well9_true_tvd_m, atol=1)
    np.testing.assert_allclose(mE9, well9_true_easting, atol=1)
    np.testing.assert_allclose(mN9, well9_true_northing, atol=1)
    np.testing.assert_allclose(tvd10, well10_true_tvd_m, atol=5)
    np.testing.assert_allclose(mE10, well10_true_easting, atol=85)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=10)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=10)

def test_position_log_interface_mincurve():
    """
    This pretty much only tests the mincurve, but packed in the
    deviation+position_log interface
    """
    md = well9_true_md_m
    inc = well9_true_inc
    azi = well9_true_azi

    dev = deviation(md, inc, azi)
    pos = dev.minimum_curvature()
    pos = pos.resample(depths = md)
    pos.to_wellhead(surface_northing = 39998.454, surface_easting = 655701.278, inplace = True)

    np.testing.assert_allclose(pos.depth,    well9_true_tvd_m,    atol=1)
    np.testing.assert_allclose(pos.northing, well9_true_northing, atol=1)
    np.testing.assert_allclose(pos.easting,  well9_true_easting,  atol=1)

def test_roundtrip(atol = 0.01):
    """
    This pretty much only tests the mincurve, but packed in the
    deviation+position_log interface
    """
    md = well9_true_md_m
    inc = well9_true_inc
    azi = well9_true_azi

    dev = deviation(md, inc, azi)
    pos = dev.minimum_curvature()
    dev2 = pos.deviation()
    np.testing.assert_allclose(dev.md,  dev2.md,  atol = atol)
    np.testing.assert_allclose(dev.inc, dev2.inc, atol = atol)
    np.testing.assert_allclose(dev.azi, dev2.azi, atol = atol)

    pos.to_wellhead(surface_northing = 39998.454, surface_easting = 655701.278, inplace = True)
    np.testing.assert_allclose(pos.depth,    well9_true_tvd_m,    atol=1)
    np.testing.assert_allclose(pos.northing, well9_true_northing, atol=1)
    np.testing.assert_allclose(pos.easting,  well9_true_easting,  atol=1)
