import pytest
import numpy as np

from ..mincurve import minimum_curvature

# inputs are array-like
def test_md_throws():
    with pytest.raises(ValueError):
        _ = minimum_curvature(md='lmkcde', inc=[1,2,3], azi=[1,2,3])

def test_inc_throws():
    with pytest.raises(ValueError):
        _ = minimum_curvature(md=[1,2,3], inc='adsda', azi=[1,2,3])

def test_azi_throws():
    with pytest.raises(ValueError):
        _ = minimum_curvature(md=[1,2,3], inc=[1,2,3], azi='kjnef')

# inputs are same length
def test_input_lengths_throws():
    with pytest.raises(ValueError):
        _ = minimum_curvature(md=[1,2,3], inc=[1,2,3], azi=[1,2])

# md array increases strictly at each step
def test_increasing_md_throws():
    with pytest.raises(ValueError):
        _ = minimum_curvature(md=[1,1,3], inc=[1,2,3], azi=[1,2,3])

# get normalising for dls
def test_bad_normalising_throws():
    with pytest.raises(TypeError):
        _ = minimum_curvature(md=[1,2,3], inc=[1,2,3], azi=[1,2,3], course_length='0')
