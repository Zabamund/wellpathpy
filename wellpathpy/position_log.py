import numpy as np

from .checkarrays import checkarrays
from .mincurve import minimum_curvature as mincurve
from . import location
from . import geometry

class deviation:
    """Deviation

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
    def __init__(self, src, depth, northing, easting):
        """

        Parameters
        ----------
        src : deviation
        tvd : array_like
        northing : array_like
        easting : array_like
        """
        self.source = src.copy()
        self.depth = depth
        self.northing = northing
        self.easting = easting
        self.resampled_md = None

    def copy(self):
        l = position_log(self.source, np.copy(self.depth), np.copy(self.northing), np.copy(self.easting))
        if self.resampled_md is not None:
            l.resampled_md = np.copy(self.resampled_md)
        return l

    def to_wellhead(self, surface_northing, surface_easting):
        """Create a new position log instance moved to the wellhead location

        Parameters
        ----------
        surface_northing : array_like
        surface_easting : array_like
        """

        depth, n, e = location.loc_to_wellhead(
            self.depth,
            self.northing,
            self.easting,
            surface_northing,
            surface_easting,
        )

        self.depth = depth
        self.northing = n
        self.easting = e

    def resample(self, *args, **kwargs):
        raise NotImplementedError

    def deviation(self, *args, **kwargs):
        raise NotImplementedError

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
    omega = geometry.angle_between(p0, p1)
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
    def __init__(self, src, depth, n, e, dls):
        super().__init__(src, depth, n, e)
        self.dls = dls

    def copy(self):
        l = minimum_curvature(self.source, np.copy(self.depth), np.copy(self.northing), np.copy(self.easting), np.copy(self.dls))
        if self.resampled_md is not None:
            l.resampled_md = np.copy(self.resampled_md)
        return l

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

        >>> depths = list(range(int(dev.md[-1]) + 1))
        >>> resampled = pos.resample(depths = depths)
        """
        # break the well path into its survey stations, upper and lower, and
        # consider the well path between two stations a curve, the edge of a
        # circle, between them. Interpolate each of these segments
        # individually, and stack the results.

        depths = np.asarray(depths)
        nve = np.column_stack([self.northing, self.easting, self.depth])
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
            depth = xs[:, 2],
            n   = xs[:, 0],
            e   = xs[:, 1],
            dls = self.dls,
        )
        pos.resampled_md = np.array(depths, copy = True)
        return pos

    def deviation(self):
        """Deviation survey

        Compute an approximate deviation survey from the position log, i.e. the
        measured that would be convertable to this well path. It is assumed
        that inclination, azimuth, and measured-depth starts at 0.

        Returns
        -------
        dev : deviation
        """

        upper = zip(self.northing[:-1], self.easting[:-1], self.depth[:-1])
        lower = zip(self.northing[1:],  self.easting[1:],  self.depth[1:])

        """
        The implementation is based on this [1] stackexchange answer by tma,
        which is included verbatim for future reference.

            In order to get a better picture you should look at the problem in
            2d. Your arc from (x1,y1,z1) to (x2,y2,z2) lives in a 2d plane,
            also in the same pane the tangents (a1,i1) and (a2, i2). The 2d
            plane is given by the vector (x1,y1,y3) to (x2,y2,z2) and vector
            converted from polar to Cartesian of (a1, i1). In case their
            co-linear is just a straight line and your done. Given the angle
            between the (x1,y1,z2) and (a1, i1) be alpha, then the angle
            between (x2,y2,z2) and (a2, i2) is –alpha. Use the normal vector of
            the 2d plane and rotate normalized vector (x1,y1,z1) to (x2,y2,z2)
            by alpha (maybe –alpha) and converter back to polar coordinates,
            which gives you (a2,i2). If d is the distance from (x1,y1,z1) to
            (x2,y2,z2) then MD = d* alpha /sin(alpha).

        In essence, the well path (in cartesian coordinates) is evaluated in
        segments from top to bottom, and for every segment the inclination and
        azimuth "downwards" are reconstructed. The reconstructed inc and azi is
        used as "entry angle" of the well bore into the next segment. This uses
        some assumptions deriving from knowing that the position log was
        calculated with the min-curve method, since a straight
        cartesian-to-spherical conversion could be very sensitive [2].

        [1] https://math.stackexchange.com/a/1191620
        [2] I observed low error on average, but some segments could be off by
            80 degrees azimuth
        """

        # Assume the initial depth and angles are all zero, but this can likely
        # be parametrised.
        incs, azis, mds = [0], [0], [0]
        i1, a1 = 0, 0

        for up, lo in zip(upper, lower):
            up = np.array(up)
            lo = np.array(lo)

            # Make two vectors
            # v1 is the vector from the upper survey station to the lower
            # v2 is the vector formed by the initial inc/azi (given by the
            # previous iteration).
            #
            # The v1 and v2 vectors form a plane the well path arc lives in.
            v1 = lo - up
            v2 = np.array(geometry.direction_vector(i1, a1))

            alpha  = geometry.angle_between(v1, v2)
            normal = geometry.normal_vector(v1, v2)

            # v3 is the "exit vector", i.e. the direction of the well bore
            # at the lower survey station, which would in turn be "entry
            # direction" in the next segment.
            v3 = geometry.rotate(v1, normal, -alpha)
            i2, a2 = geometry.spherical(*v3)

            # d is the length of the vector (straight line) from the upper
            # station to the lower station.
            d = np.linalg.norm(v1)
            incs.append(i2)
            azis.append(a2)
            mds.append(d * alpha / np.sin(alpha))
            # The current lower station is the upper station in the next
            # segment.
            i1 = i2
            a1 = a2

        mds = np.cumsum(mds)
        return deviation(
            md  = np.array(mds),
            inc = np.array(incs),
            azi = np.array(azis),
        )
