import pytest
from wellpathpy.wellpath import read_deviation
import pandas as pd

TEST_DATA = "wellpathpy/test/fixtures/Well_Surveys_Projected_to_TD.csv"


def test_read_deviation():

    dev_df = read_deviation(TEST_DATA)

    assert isinstance(dev_df, pd.DataFrame)
