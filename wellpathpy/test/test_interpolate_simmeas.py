import pytest
import numpy as np
import pandas as pd
import similaritymeasures as sim

from ..interpolate import interpolate_deviation, interpolate_position

# interpolation is close to input data

# import test well data
well9 = pd.read_csv('./wellpathpy/test/fixtures/well9.csv', sep=",")
well10 = pd.read_csv('./wellpathpy/test/fixtures/well10.csv', sep=",")

# get data series
well9_true_md = well9['Measured Depth ( ft )'].values
well9_true_md_index = np.arange(0, well9_true_md.size, 1)
well9_true_inc = well9['Inclination ( deg )'].values
well9_true_inc_index = np.arange(0, well9_true_inc.size, 1)
well9_true_azi = well9['Azimuth Grid ( deg )'].values
well9_true_azi_index = np.arange(0, well9_true_azi.size, 1)
well9_true_tvd = well9['TVD ( ft )'].values
well9_true_tvd_index = np.arange(0, well9_true_tvd.size, 1)
well9_true_northing = well9['Northing ( m )'].values
well9_true_northing_index = np.arange(0, well9_true_northing.size, 1)
well9_true_easting = well9['Easting ( m )'].values
well9_true_easting_index = np.arange(0, well9_true_easting.size, 1)

well10_true_md = well10['Measured Depth ( ft )'].values
well10_true_md_index = np.arange(0, well10_true_md.size, 1)
well10_true_inc = well10['Inclination ( deg )'].values
well10_true_inc_index = np.arange(0, well10_true_inc.size, 1)
well10_true_azi = well10['Azimuth Grid ( deg )'].values
well10_true_azi_index = np.arange(0, well10_true_azi.size, 1)
well10_true_tvd = well10['TVD ( ft )'].values
well10_true_tvd_index = np.arange(0, well10_true_tvd.size, 1)
well10_true_northing = well10['Northing ( m )'].values
well10_true_northing_index = np.arange(0, well10_true_northing.size, 1)
well10_true_easting = well10['Easting ( m )'].values
well10_true_easting_index = np.arange(0, well10_true_easting.size, 1)

# format data series
# Generate raw data
curve_values_raw = well9_true_md
curve_index_raw = well9_true_md_index
exp_data = np.zeros((curve_index_raw.size, 2))
exp_data[:, 0] = curve_index_raw
exp_data[:, 1] = curve_values_raw

# Generate interpolated data
curve_values_int, _, _ = interpolate_deviation(well9_true_md, well9_true_inc, well9_true_azi, md_step=1)
curve_index_int = np.arange(0,curve_values_int.size,1)
num_data = np.zeros((curve_index_int.size, 2))
num_data[:, 0] = curve_index_int
num_data[:, 1] = curve_values_int

def test_w9_dev_md():
    dtw, _ = sim.dtw(exp_data, num_data)
    print(f'dtw: {dtw}')
    np.testing.assert_allclose(dtw, 0, atol=20)