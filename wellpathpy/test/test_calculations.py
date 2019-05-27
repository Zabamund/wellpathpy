import pytest
import pandas as pd
import numpy as np

from ..tan import tan_method
from ..mincurve import min_curve_method
from ..rad_curv import rad_curve_method

# mock data set from Crain's Petrophysical handbook
# https://www.spec2000.net/19-dip13.htm

# Make sure the relative path is set from location where `python setup.py test` is run
mock_df = pd.read_csv('./wellpathpy/test/fixtures/mock_data_set.csv')
mock_md = mock_df['md'].values
mock_inc = mock_df['inc'].values
mock_azi = mock_df['azi'].values

# mock data solution from Crain's Petrophysical handbook
# https://www.spec2000.net/19-dip13.htm
true_high_tan_mN = mock_df['mN_ht'].values
true_high_tan_mE = mock_df['mE_ht'].values
true_high_tan_TVD = mock_df['tvd_ht'].values

true_low_tan_mN = mock_df['mN_lt'].values
true_low_tan_mE = mock_df['mE_lt'].values
true_low_tan_TVD = mock_df['tvd_lt'].values

true_avg_tan_mN = mock_df['mN_avg'].values
true_avg_tan_mE = mock_df['mE_avg'].values
true_avg_tan_TVD = mock_df['tvd_avg'].values

true_bal_tan_mN = mock_df['mN_bal'].values
true_bal_tan_mE = mock_df['mE_bal'].values
true_bal_tan_TVD = mock_df['tvd_bal'].values

true_min_curve_mN = mock_df['mN_minc'].values
true_min_curve_mE = mock_df['mE_minc'].values
true_min_curve_TVD = mock_df['tvd_minc'].values
true_min_curve_dls = mock_df['dl'].values

true_rad_curve_mN = mock_df['mN_radc'].values
true_rad_curve_mE = mock_df['mE_radc'].values
true_rad_curve_TVD = mock_df['tvd_radc'].values

# test methods
def test_high_tan():
    tvd, mN, mE = tan_method(mock_md, mock_inc, mock_azi, choice='high')
    np.testing.assert_allclose(tvd, true_high_tan_TVD)
    np.testing.assert_allclose(mE, true_high_tan_mE)
    np.testing.assert_allclose(mN, true_high_tan_mN)

def test_low_tan():
    tvd, mN, mE = tan_method(mock_md, mock_inc, mock_azi, choice='low')
    np.testing.assert_allclose(tvd, true_low_tan_TVD)
    np.testing.assert_allclose(mE, true_low_tan_mE)
    np.testing.assert_allclose(mN, true_low_tan_mN)

def test_avg_tan():
    tvd, mN, mE = tan_method(mock_md, mock_inc, mock_azi, choice='avg')
    np.testing.assert_allclose(tvd, true_avg_tan_TVD, atol=1)
    np.testing.assert_allclose(mE, true_avg_tan_mE, atol=5)
    np.testing.assert_allclose(mN, true_avg_tan_mN, atol=5)

def test_bal_tan():
    tvd, mN, mE = tan_method(mock_md, mock_inc, mock_azi, choice='bal')
    np.testing.assert_allclose(tvd, true_bal_tan_TVD)
    np.testing.assert_allclose(mE, true_bal_tan_mE)
    np.testing.assert_allclose(mN, true_bal_tan_mN)

def test_min_curve():
    tvd, mN, mE, dls = min_curve_method(mock_md, mock_inc, mock_azi, norm_opt=1)
    np.testing.assert_allclose(tvd, true_min_curve_TVD, atol=1)
    np.testing.assert_allclose(mE, true_min_curve_mE, atol=5)
    np.testing.assert_allclose(mN, true_min_curve_mN, atol=5)
    np.testing.assert_allclose(dls, true_min_curve_dls, atol=1)

def test_rad_curve():
    #tvd, mN, mE = rad_curve_method(mock_md, mock_inc, mock_azi)
    #print(f'test_output:\ntvd:{tvd}\ntrue_rad_curve_TVD:{true_rad_curve_TVD}')
    #np.testing.assert_allclose(tvd, true_rad_curve_TVD, atol=1)
    #print(f'test_output:\nmE:{mE}\ntrue_rad_curve_mE:{true_rad_curve_mE}')
    #np.testing.assert_allclose(mE, true_rad_curve_mE, atol=5)
    #print(f'test_output:\nmN:{mN}\ntrue_rad_curve_mN:{true_rad_curve_mN}')
    #np.testing.assert_allclose(mN, true_rad_curve_mN, atol=5)
    pass