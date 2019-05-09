# -*- coding: utf 8 -*-
"""
Define a suite a tests for the deviation calculations.
"""
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pylab as plt


# Some globals.
DNAME = "data/Well_Surveys_Projected_to_TD.csv"


def nrmse(measured, actual):

    range = np.max(actual) - np.min(actual)
    if range == 0:
        return 0
    else:
        return np.sqrt(((measured - actual) ** 2).mean()) / (
            np.max(actual) - np.min(actual)
        )


def compare_curve(new_curve, true_curve):

    return nrmse(new_curve, true_curve)


def tan_method(md, inc, azi):

    azi_r = np.deg2rad(azi)
    inc_r = np.deg2rad(inc)

    northing = np.cumsum((md[1:] - md[:-1]) * np.sin(inc_r[1:]) * np.cos(azi_r[1:]))
    northing = np.insert(northing, 0, 0)

    easting = np.cumsum((md[1:] - md[:-1]) * np.sin(inc_r[1:]) * np.sin(azi_r[1:]))
    easting = np.insert(easting, 0, 0)

    tvd = np.cumsum((md[1:] - md[:-1]) * np.cos(inc_r[1:]))
    tvd = np.insert(tvd, 0, 0)

    return tvd, northing, easting


def run_tests():
    true_df = pd.read_csv(
        DNAME, header=4, skipfooter=3, index_col=False, engine="python"
    ).dropna(axis=1)

    # true_data = {'MD[m]': [0, 10, 20, 30, 40],
    #              'Inc[deg]': [0, 10, 10, 10, 10],
    #              'Azi[deg]': [0, 0, 0, 0, 0],
    #              'North[m]': [0.0, 1.7, 3.5, 5.2, 6.9],
    #              'East[m]': [0.0, 0.0, 0.0, 0.0, 0.0],
    #              'TVD[m]': [0.0, 9.8, 19.7, 29.5, 39.4]}

    # true_df = pd.DataFrame(true_data)

    md = true_df["MD[m]"].values
    inc = true_df["Inc[deg]"].values
    azi = true_df["Azi[deg]"].values

    true_northing = true_df["North[m]"]
    true_easting = true_df["East[m]"]
    true_tvd = true_df["TVD[m]"]

    tvd, northing, easting = tan_method(md, inc, azi)

    print("TVD Error: ", compare_curve(tvd, true_tvd))
    print("North Error: ", compare_curve(northing, true_northing))
    print("East Error: ", compare_curve(easting, true_easting))

    assert np.allclose(tvd, true_tvd, rtol=1e-2)

    fig = plt.figure()
    ax = fig.gca(projection="3d")

    ax.plot(easting, northing, tvd, label="test well")
    ax.plot(true_easting, true_northing, true_tvd, label="true well")

    ax.invert_zaxis()
    ax.legend()
    plt.show()


if __name__ == "__main__":
    run_tests()
