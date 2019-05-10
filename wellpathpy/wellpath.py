# class WellPath(self):

#     self.northing
#     self.easting
#     self.tvd

#     self.md
#     self.inclination
#     self.azimuth

import pandas as pd


def read_deviation(filename):
    """
    Read a csv file with md, inc and az, return a dataframe with deviation
    """
    deviation_df = pd.read_csv(filename).dropna(axis=0)

    return deviation_df


# input, dataframe with MD, INC and AZ
# output, dataframe with TVD, N, E added
def dev2path(
    dev,
    md_label="MD",
    inc_label="INC",
    az_label="AZ",
    north_label="NORTHING",
    east_label="EASTING",
    tvd_label="TVD",
    method="tan",
):

    md = dev[md_label].values
    inc = dev[inc_label].values
    azi = dev[az_label].values

    tvd, northing, easting = tan_method(md, inc, azi)

    dev_loc = dev.copy()

    dev_loc[tvd_label] = tvd
    dev_loc[north_label] = northing
    dev_loc[east_label] = easting

    return dev_loc
