import pytest
import io

from ..read import read_csv

good_data = '''md,inc,azi
    0,0,244
    1,11,220
    2,13,254
    3,15,258'''

renamed_cols = '''measured-depth,inci,am
    0,0,244
    1,11,220
    2,13,254
    3,15,258'''

xtra_cols = '''md,inc,azi,tvd
    0,0,244,0
    1,11,220,21
    2,13,254,23
    3,15,258,25'''

too_few_columns = '''md,inc
    0,0
    1,11
    2,13
    3,15'''

not_monotonic_md = '''md,inc,azi
    0,0,244
    1,11,220
    3,13,254
    2,15,258'''

def test_all_cols_present():
    # should pass if md, inc and azi are present
    data = io.StringIO(good_data)
    _ = read_csv(data)

def test_too_many_columns():
    # should pass if md, inc and azi are present even if other cols present
    data = io.StringIO(xtra_cols)
    _ = read_csv(data)

def test_too_few_columns():
    # should fail if few than three columns passed
    data = io.StringIO(too_few_columns)
    with pytest.raises(ValueError):
        _ = read_csv(data)

def test_inc_in_range_raise():
    # should fail if inc values not within 0-180
    inc_low = good_data.replace(',11,', ',-11,')
    data = io.StringIO(inc_low)
    with pytest.raises(ValueError):
        _ = read_csv(data)
    inc_high = good_data.replace(',11,', ',181,')
    data = io.StringIO(inc_high)
    with pytest.raises(ValueError):
        _ = read_csv(data)

def test_azi_in_range_throws():
    # should fail if azi values not within 0-360
    azi_low = good_data.replace(',244', ',-244')
    data = io.StringIO(azi_low)
    with pytest.raises(ValueError):
        _ = read_csv(data)
    azi_high = good_data.replace(',244', ',2440')
    data = io.StringIO(azi_high)
    with pytest.raises(ValueError):
        _ = read_csv(data)

def test_checkarrays_not_monotonic_md_throws():
    # should fail if checkarrays fails on md
    data = io.StringIO(not_monotonic_md)
    with pytest.raises(ValueError):
        _ = read_csv(data)

def test_nans_throws():
    # should fail if nans in input
    nans_present_md = good_data.replace('3,15,258', 'NaN,15,258')
    nans_present_inc = good_data.replace('3,15,258', '3,NaN,258')
    nans_present_azi = good_data.replace('3,15,258', '3,15,NaN')
    for nans_present in [nans_present_md, nans_present_inc, nans_present_azi]:
        data = io.StringIO(nans_present)
        with pytest.raises(ValueError):
            _ = read_csv(data)

def test_renamed_columns():
    data = io.StringIO(renamed_cols)
    _ = read_csv(data)
