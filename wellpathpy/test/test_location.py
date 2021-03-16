import pytest
import numpy as np

from ..mincurve import minimum_curvature
from ..location import loc_to_wellhead, loc_to_zero, loc_to_tvdss

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

def test_wellhead():
    # test well9
    well9_tvd, well9_northing, well9_easting, _ = minimum_curvature(well9_true_md_m, well9_true_inc, well9_true_azi)
    tvd, mN, mE = loc_to_wellhead(
        well9_tvd,
        well9_northing,
        well9_easting,
        well9_true_surface_northing,
        well9_true_surface_easting
        )
    np.testing.assert_equal(tvd, well9_tvd)
    np.testing.assert_allclose(mN, well9_true_northing, atol=1)
    np.testing.assert_allclose(mE, well9_true_easting, atol=1)
    # test well10
    well10_tvd, well10_northing, well10_easting, _ = minimum_curvature(well10_true_md_m, well10_true_inc, well10_true_azi)
    tvd, mN, mE = loc_to_wellhead(
        well10_tvd,
        well10_northing,
        well10_easting,
        well10_true_surface_northing,
        well10_true_surface_easting
        )
    np.testing.assert_equal(tvd, well10_tvd)
    np.testing.assert_allclose(mN, well10_true_northing, atol=1)
    np.testing.assert_allclose(mE, well10_true_easting, atol=1)

def test_zero():
    # test well9
    _, well9_northing, well9_easting, _ = minimum_curvature(well9_true_md_m, well9_true_inc, well9_true_azi)
    tvd, mN, mE = loc_to_zero(
        well9_true_tvd_m,
        well9_true_northing,
        well9_true_easting,
        well9_true_surface_northing,
        well9_true_surface_easting
        )
    np.testing.assert_equal(tvd, well9_true_tvd_m)
    np.testing.assert_allclose(mN, well9_northing, atol=1)
    np.testing.assert_allclose(mE, well9_easting, atol=1)
    # test well10
    _, well10_northing, well10_easting, _ = minimum_curvature(well10_true_md_m, well10_true_inc, well10_true_azi)
    tvd, mN, mE = loc_to_zero(
        well10_true_tvd_m,
        well10_true_northing,
        well10_true_easting,
        well10_true_surface_northing,
        well10_true_surface_easting
        )
    np.testing.assert_equal(tvd, well10_true_tvd_m)
    np.testing.assert_allclose(mN, well10_northing, atol=1)
    np.testing.assert_allclose(mE, well10_easting, atol=1)

def test_tvdss():
    # test well9
    well9_tvd, well9_northing, well9_easting, _ = minimum_curvature(well9_true_md_m, well9_true_inc, well9_true_azi)
    tvdss, mN, mE = loc_to_tvdss(
        well9_tvd,
        well9_northing,
        well9_easting,
        well9_true_datum_elevation
        )
    np.testing.assert_allclose(tvdss, well9_true_datum_elevation - well9_true_tvd_m)
    np.testing.assert_equal(mN, well9_northing)
    np.testing.assert_equal(mE, well9_easting)
    # test well10
    well10_tvd, well10_northing, well10_easting, _ = minimum_curvature(well10_true_md_m, well10_true_inc, well10_true_azi)
    tvdss, mN, mE = loc_to_tvdss(
        well10_tvd,
        well10_northing,
        well10_easting,
        well10_true_datum_elevation
        )
    np.testing.assert_allclose(tvdss, well10_true_datum_elevation - well10_true_tvd_m)
    np.testing.assert_equal(mN, well10_northing)
    np.testing.assert_equal(mE, well10_easting)