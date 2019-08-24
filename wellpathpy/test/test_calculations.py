import pytest
import pandas as pd
import numpy as np

from ..tan import tan_method
from ..mincurve import minimum_curvature
from ..rad_curv import rad_curve_method
from ..location import loc_to_wellhead

# import test well data
well9 = pd.read_csv('./wellpathpy/test/fixtures/well9.csv', sep=",")
well10 = pd.read_csv('./wellpathpy/test/fixtures/well10.csv', sep=",")

# get data series
well9_true_md_m = well9['Measured Depth ( ft )'].values * 0.3048 # converting feet to meters
well9_true_inc = well9['Inclination ( deg )'].values
well9_true_azi = well9['Azimuth Grid ( deg )'].values
well9_true_tvd_m = well9['TVD ( ft )'].values * 0.3048 # converting feet to meters
well9_true_northing = well9['Northing ( m )'].values
well9_true_easting = well9['Easting ( m )'].values
well9_true_dls = well9['DLS ( deg/100 ft )'].values
well9_true_surface_northing = 39998.454
well9_true_surface_easting = 655701.278
well9_true_datum_elevation = 100 * 0.3048 # converting feet to meters

well10_true_md_m = well10['Measured Depth ( ft )'].values * 0.3048 # converting feet to meters
well10_true_inc = well10['Inclination ( deg )'].values
well10_true_azi = well10['Azimuth Grid ( deg )'].values
well10_true_tvd_m = well10['TVD ( ft )'].values * 0.3048 # converting feet to meters
well10_true_northing = well10['Northing ( m )'].values
well10_true_easting = well10['Easting ( m )'].values
well10_true_dls = well10['DLS ( deg/100 ft )'].values
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

def test_rad_curve():
    tvd9, mN9, mE9 = rad_curve_method(well9_true_md_m, well9_true_inc, well9_true_azi)
    tvd10, mN10, mE10 = rad_curve_method(well10_true_md_m, well10_true_inc, well10_true_azi)
    tvd9, mN9, mE9 = loc_to_wellhead(tvd9, mN9, mE9, 39998.454, 655701.278)
    tvd10, mN10, mE10 = loc_to_wellhead(tvd10, mN10, mE10, 40004.564, 655701.377)
    np.testing.assert_allclose(tvd9, well9_true_tvd_m, atol=1)
    np.testing.assert_allclose(mE9, well9_true_easting, atol=1)
    np.testing.assert_allclose(mN9, well9_true_northing, atol=1)
    np.testing.assert_allclose(tvd10, well10_true_tvd_m, atol=5)
    np.testing.assert_allclose(mE10, well10_true_easting, atol=85)
    np.testing.assert_allclose(mN10, well10_true_northing, atol=10)