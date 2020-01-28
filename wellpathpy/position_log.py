import numpy as np

from .checkarrays import checkarrays
from .geometry import spherical
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
        self.resampled_md = None

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

    def deviation(self, *args, **kwargs):
        raise NotImplementedError

def normalize(x):
    """
    Normalize is in addition to zeros also sensitive to *very* small floats.

        Falsifying example: deviation_survey=(
            md = array([0.0000000e+000, 1.0000000e+000, 4.1242594e-162]),
            inc = array([0., 0., 0.]),
            azi = array([0., 0., 0.]))

    yields a dot product of 1.0712553822854385, which is outside [-1, 1]. This
    should *really* only show up in testing scenarios and not real data.

    Whenever norm values are less than eps, consider them zero. All zero norms
    are assigned 1, to avoid divide-by-zero. The value for zero is chosen
    arbitrarily as a something that shouldn't happen in real data, or when it
    does is reasonable to consier as zero.
    """
    norm = np.atleast_1d(np.linalg.norm(x))
    zero = 1e-15
    norm[np.abs(norm) < zero] = 1.0
    return x / norm

def spherical_interpolate(p0, p1, t):
    """
    https://en.wikipedia.org/wiki/Slerp

    It's important that the interpolation method used when resampling
    corresponds to the model used for calculating the well path. For the
    minimum curvature, spherical interpolation is a good fit. This is pretty
    much a carbon copy, geometrical implementation from the wikipedia formula.

    Parameters
    ----------
    p0 : array_like
        First points on the arc, in (northing, easting, tvd)
    p1 : array_like
        Last points  on the arc, in (northing, easting, tvd)
    t : array_like
        The points between p0 and p1 to return, 0 <= t <= 1

    Returns
    -------
    positions : array_like
        Resampled positions in (northing, easting, tvd)
    """
    p0unit = normalize(p0)
    p1unit = normalize(p1)
    dot = np.dot(p0unit, p1unit)
    # arccos is only defined [-1,1], dot can _sometimes_ go outside this domain
    # because of floating points
    if not -1 <= dot <= 1:
        clipped = np.clip(dot, -1, 1)
        if np.isclose(dot, clipped, atol = 1e-7, rtol = 1e-7):
            dot = clipped
        else:
            msg = 'dot product (= {}) outside of arccos domain [-1, 1]'
            raise RuntimeError(msg.format(dot))

    omega = np.arccos(dot)
    if omega != 0:
        v0 = np.sin((1 - t) * omega) / np.sin(omega)
        v1 = np.sin(     t  * omega) / np.sin(omega)
    else:
        # reduce to linear interpolation
        v0 = 1 - t
        v1 = t
    V0 = v0 * p0[:, np.newaxis]
    V1 = v1 * p1[:, np.newaxis]
    return V0 + V1

class minimum_curvature(position_log):
    def __init__(self, src, tvd, n, e, dls):
        super().__init__(src, tvd, n, e)
        self.dls = dls

    def resample(self, depths):
        """
        Resample the position log onto a new measured-depth.

        Parameters
        ----------
        depths : array_like
            The measured depths to resample onto

        Returns
        -------
        resampled : minimum_curvature
            Resampled position log

        Examples
        --------
        Resample onto a regular, 1m measured depth interval:

        >>> depths = list(range(int(dev.md[-1])) + 1)
        >>> resampled = pos.resample(depths = depths)
        """
        # break the well path into its survey stations, upper and lower, and
        # consider the well path between two stations a curve, the edge of a
        # circle, between them. Interpolate each of these segments
        # individually, and stack the results.

        depths = np.asarray(depths)
        nve = np.column_stack([self.northing, self.easting, self.tvd])
        upper = nve[:-1]
        lower = nve[1:]

        mds = self.source.md
        md_upper = mds[:-1]
        md_lower = mds[1:]

        assert len(md_upper) == len(md_lower)
        assert len(upper) == len(md_upper)
        assert len(upper) == len(lower)

        xs = []
        segments = len(md_upper)
        for i in range(segments):
            md1 = md_upper[i]
            md2 = md_lower[i]
            if i < segments - 1:
                md_i = depths[(depths >= md1) & (depths <  md2)]
            else:
                md_i = depths[(depths >= md1) & (depths <= md2)]

            t = (md_i - md1) / (md2 - md1)
            interpolated = spherical_interpolate(upper[i], lower[i], t)
            xs.append(interpolated.T)
        xs = np.concatenate(xs, axis = 0)

        pos = minimum_curvature(
            src = self.source,
            tvd = xs[:, 2],
            n   = xs[:, 0],
            e   = xs[:, 1],
            dls = self.dls,
        )
        pos.resampled_md = np.array(depths, copy = True)
        return pos
