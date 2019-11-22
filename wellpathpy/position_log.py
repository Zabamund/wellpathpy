import numpy as np

from .checkarrays import checkarrays
from .mincurve import minimum_curvature as mincurve
from . import location

class deviation:
    """

    The deviation is a glorified triple (md, inc, azi), with some interesting
    operations.

    Notes
    -----
    Glossary:
    md : measured depth
    inc : inclination (in degrees)
    azi : azimuth (in degrees)
    """
    def __init__(self, md, inc, azi):
        md, inc, azi = checkarrays(md, inc, azi)
        self.md = np.copy(md)
        self.inc = np.copy(inc)
        self.azi = np.copy(azi)

    def copy(self):
        return deviation(self.md, self.inc, self.azi)

    def minimum_curvature(self, course_length = 30):
        tvd, n, e, dls = mincurve(
            md = self.md,
            inc = self.inc,
            azi = self.azi,
            course_length = course_length,
        )
        return minimum_curvature(self, tvd, n, e, dls)

class position_log:
    """Position log

    The position log is the computed positions of the well path. It has no
    memory of the method that created it, but it knows what deviation it came
    from. In its essence, it's a glorified triplet (tvd, northing, easting)
    with some interesting operations.

    Notes
    -----
    Glossary:
    tvd : true vertical depth
    """
    def __init__(self, src, tvd, northing, easting):
        """

        Parameters
        ----------
        src : deviation
        tvd : array_like
        northing : array_like
        easting : array_like
        """
        self.source = src.copy()
        self.tvd = tvd
        self.northing = northing
        self.easting = easting

    def to_wellhead(self, surface_northing, surface_easting):
        """Shift position to wellhead location in-place

        Parameters
        ----------
        surface_northing : array_like
        surface_easting : array_like
        """
        tvd, n, e = location.loc_to_wellhead(
            self.tvd,
            self.northing,
            self.easting,
            surface_northing,
            surface_easting,
        )

        self.tvd = tvd
        self.northing = n
        self.easting = e

    def resample(self, *args, **kwargs):
        raise NotImplementedError

    def deviation(self):
        raise NotImplementedError

class minimum_curvature(position_log):
    def __init__(self, src, tvd, n, e, dls):
        super().__init__(src, tvd, n, e)
        self.dls = dls
