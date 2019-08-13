import pytest
import numpy as np

from ..rad_curv import radius_curvature

# inputs are array-like
def test_md_throws():
    with pytest.raises(ValueError):
        _ = radius_curvature(md='lmkcde', inc=[1,2,3], azi=[1,2,3])

def test_inc_throws():
    with pytest.raises(ValueError):
        _ = radius_curvature(md=[1,2,3], inc='adsda', azi=[1,2,3])

def test_azi_throws():
    with pytest.raises(ValueError):
        _ = radius_curvature(md=[1,2,3], inc=[1,2,3], azi='kjnef')

# inputs are same length
def test_input_lengths_throws():
    with pytest.raises(ValueError):
        _ = radius_curvature(md=[1,2,3], inc=[1,2,3], azi=[1,2])

# md array increases strictly at each step
def test_increasing_md_throws():
    with pytest.raises(ValueError):
        _ = radius_curvature(md=[1,1,3], inc=[1,2,3], azi=[1,2,3])