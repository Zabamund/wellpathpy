import pytest
import numpy as np

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