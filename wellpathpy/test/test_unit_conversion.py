import pytest
import numpy as np
import pint

from ..convert import unit_convert

# test inputs
def test_data_throws():
    with pytest.raises(TypeError):
        _ = unit_convert('data', src='ft', dst='m')

def test_src_throws():
    with pytest.raises(AttributeError):
        _ = unit_convert(1, src=999, dst='m')

def test_dst_throws():
    with pytest.raises(AttributeError):
        _ = unit_convert(1, src='ft', dst=999)

# test conversion
def test_ft_m():
    result = unit_convert(1, src='ft', dst='m')
    np.testing.assert_allclose(result, 0.3048)

def test_ft_m_array():
    result = unit_convert(np.arange(0,10,1), src='ft', dst='m')
    np.testing.assert_allclose(result, np.arange(0,10,1) * 0.3048)

# test ureg
def test_datum_user_unit_registry():
    ureg = pint.UnitRegistry()
    ureg.define('ell = 0.6275 * meter = ell')
    datum = 1
    result = unit_convert(datum, src='ell', dst='m', ureg=ureg)
    np.testing.assert_equal(result, 0.6275)
    
def test_array_user_unit_registry():
    ureg = pint.UnitRegistry()
    ureg.define('ell = 0.6275 * meter = ell')
    arr = np.array([0,1,2,3,4])
    result = unit_convert(arr, src='ell', dst='m', ureg=ureg)
    np.testing.assert_allclose(result, np.array([0, 0.6275, 1.255, 1.8824999999999998, 2.51]))