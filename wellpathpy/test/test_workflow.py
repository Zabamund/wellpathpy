import pytest

from .. import deviation
from .. import read_csv
from .. import unit_convert

def test_workflow_compute_mincurve():
    """
    Simple, minimal workflow over well9 - read deviation survey, and compute
    the position log with min-curve. It's a simple, but complete workflow, and
    the test checks that at least this code paths still works. The correctness
    of computation should be covered by other tests.
    """
    fname = 'wellpathpy/test/fixtures/well9.csv'
    with open(fname) as f:
        md, inc, azi = read_csv(f)

    md = unit_convert(md, src = 'ft', dst ='m')
    dev = deviation(md, inc, azi)
    pos = dev.minimum_curvature(course_length = 30)
    pos.to_wellhead(39998.454, 655701.278, inplace = True)

    # expected reference values, from the last row of the CSV
    # simple sanity checks so it's not all bonkers
    expected_tvd  = 3489.3174919404673 * 0.3048
    expected_easting = 655870.4178517371
    expected_northing = 38631.13241000773
    expected_dls = 0.871150714388663
    assert pos.depth[-1] == pytest.approx(expected_tvd)
    assert pos.northing[-1] == pytest.approx(expected_northing, abs = 0.5)
    assert pos.easting[-1] == pytest.approx(expected_easting)
    assert pos.dls[-1] == pytest.approx(expected_dls, abs = 1)
