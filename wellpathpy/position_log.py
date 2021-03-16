import numpy as np

from .checkarrays import checkarrays
from .mincurve import minimum_curvature as mincurve
from .rad_curv import radius_curvature as radcurve
from .tan import tan_method as tanmethod
from .write import deviation_to_csv, position_to_csv
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
        """This function calls mincurve.minimum_curvature with self

        Notes
        -----
            You can access help with `wp.mincurve.minimum_curvature?`
            in `ipython`
        """
        tvd, n, e, dls = mincurve(
            md = self.md,
            inc = self.inc,
            azi = self.azi,
            course_length = course_length,
        )
        return minimum_curvature(self, tvd, n, e, dls)

    def radius_curvature(self):
        """This function calls rad_curv.radius_curvature with self

        Notes
        -----
            You can access help with `wp.rad_curv.radius_curvature?`
            in `ipython`
        """
        tvd, n, e = radcurve(
            md = self.md,
            inc = self.inc,
            azi = self.azi
        )
        return radius_curvature(self, tvd, n, e)

    def tan_method(self, choice = 'avg'):
        """This function calls tan.tan_method with self

        Notes
        -----
            You can access help with `wp.tan.tan_method?`
            in `ipython`
        """
        tvd, n, e = tanmethod(
            md = self.md,
            inc = self.inc,
            azi = self.azi,
            choice = choice,
        )
        return tan_method(self, tvd, n, e)

    def to_csv(self, fname, **kwargs):
        """This function calls write.deviation_to_csv with self

        Notes
        -----
            You can access help with `wp.write.deviation_to_csv?`
            in `ipython`
        """
        return deviation_to_csv(fname, self.md, self.inc, self.azi, **kwargs)

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

    def copy(self):
        l = position_log(self.source, np.copy(self.depth), np.copy(self.northing), np.copy(self.easting))
        return l

    def to_wellhead(self, surface_northing, surface_easting, inplace = False):
        """Create a new position log instance moved to the wellhead location

        Parameters
        ----------
        surface_northing : array_like
        surface_easting : array_like
        inplace : bool
        """
        if inplace:
            copy = self
        else:
            copy = self.copy()

        depth, n, e = location.loc_to_wellhead(
            copy.depth,
            copy.northing,
            copy.easting,
            surface_northing,
            surface_easting,
        )

        copy.depth = depth
        copy.northing = n
        copy.easting = e

        return copy

    def loc_to_zero(self, surface_northing, surface_easting, inplace = False):
        """Create a new position log instance moved to 0m North and 0m East

        Parameters
        ----------
        surface_northing : array_like
        surface_easting : array_like
        inplace : bool
        """
        if inplace:
            copy = self
        else:
            copy = self.copy()

        depth, n, e = location.loc_to_zero(
            copy.depth,
            copy.northing,
            copy.easting,
            surface_northing,
            surface_easting,
        )

        copy.depth = depth
        copy.northing = n
        copy.easting = e

        return copy

    def loc_to_tvdss(self, datum_elevation, inplace = False):
        """This function calls location.location_to_tvdss with self

        Notes
        -----
            You can access help with `wp.location.loc_to_tvdss?`
            in `ipython`
        """
        if inplace:
            copy = self
        else:
            copy = self.copy()

        depth, n, e = location.loc_to_tvdss(
            copy.depth,
            copy.northing,
            copy.easting,
            datum_elevation,
        )

        copy.depth = depth
        copy.northing = n
        copy.easting = e

        return copy

    def resample(self, *args, **kwargs):
        raise NotImplementedError

    def deviation(self, *args, **kwargs):
        raise NotImplementedError

    def to_csv(self, fname, **kwargs):
        """This function calls write.position_to_csv with self

        Notes
        -----
            You can access help with `wp.write.position_to_csv?`
            in `ipython`
        """
        return position_to_csv(fname, self.depth, self.northing, self.easting, **kwargs)

def spherical_interpolate(p0, p1, t, omega):
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
    omega : float
        The angle subtended by the arc

    Returns
    -------
    positions : array_like
        Resampled positions in (northing, easting, tvd)
    """
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
        # This function uses a lot of geometry, and is easier to follow
        # when able to see the shapes, vectors, and lines. There is a geogebra
        # [1] project checked [2] in, which draws the arc, chord, sphere and
        # tangents at an arbitrary segment.
        #
        # The geogebra file can be viewed through with a geogebra client, or in
        # their web client [3].
        #
        # In maths terms, resampling is done by breaking the well back into
        # segments between the (measured) survey stations in (inc, azi).
        # The line from the upper station (A) to the lower (B) is a chord on a
        # sphere, to which the vectors derived from the inclination and azimuth
        # at A and B are tangential. The arc between A and B is interpolated.
        #
        # The spherical_interpolate function takes the two points A and B, but
        # assumes that A and B have their origin in the centre of the sphere,
        # but A and B as given have their centre in the cartesian (0, 0, 0). To
        # address this, the centre of the circle is determined through a dance
        # of cross products, see the geogebra file [2]. It boils down to
        # finding the normal unit vector to either tangent with direction
        # towards the centre (C) of the sphere.
        #
        # To make it easier to follow the geometry, and map it back to
        # illustration, variable names are generally capital letters and in
        # terms of geometry.
        #
        # [1] https://www.geogebra.org/
        # [2] wellpathpy/docs/arc-interpolation.ggb
        # [3] https://www.geogebra.org/3d

        depths = np.asarray(depths)
        nve = np.column_stack([self.northing, self.easting, self.depth])
        upper = nve[:-1]
        lower = nve[1:]

        mds = self.source.md
        md_upper = mds[:-1]
        md_lower = mds[1:]

        A  = upper
        B  = lower
        AB = B - A

        # The inc/azis, gives tangents of the arc, for every segment
        incs = self.source.inc
        azis = self.source.azi
        Ts  = np.column_stack(geometry.direction_vector(incs, azis))
        Tup = Ts[:-1]
        Tlo = Ts[1:]
        Tco = geometry.normalize(np.cross(Tup, Tlo))
        N   = geometry.normalize(np.cross(Tlo, Tco))

        # The angle alpha = <(AB,Tup) is identicial to the angle <(AB,Tlo).
        # Since AC and AB are both perpendicular to the tangents Tup and Tlo,
        # the angle <CAB and <ABC is given by (pi/2 - alpha). This gives the
        # angle omega = 2*alpha, the angle subtended by the arc, which is the
        # parameter to the interpolation.
        #
        # For an illustration with these names in 2D, see
        # wellpathpy/docs/arc.png
        alpha = geometry.angle_between(AB, Tup)
        omega = 2 * alpha
        # If the angle is zero, the hole is straight and arc is undefined.
        # Handling this well probably needs a better check, and a good test
        # suite backing it
        sinalpha = 2 * np.sin(alpha)
        sinalpha.ravel()[sinalpha.ravel() == 0] = 1
        radius = np.linalg.norm(AB, axis = 1) / sinalpha
        # Get the centre of the sphere by following the selected normal vector
        # by the length of the radius. The N is normal, but in opposite
        # direction (it has the direction from centre to surface, but we want
        # from surface to centre)
        C = B - N * radius[:, np.newaxis]

        # P0 and P1 are the points at the start/end of the arc and chord, but
        # "moved" to be relative to the origin (0, 0, 0) rather than C, the
        # centre of the sphere
        P0 = A - C
        P1 = B - C

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

            # t are the points (0 <= t <= 1) on the arc to interpolate
            t = (md_i - md1) / (md2 - md1)
            log = spherical_interpolate(P0[i], P1[i], t, omega[i])
            log = log + C[i, :, np.newaxis]
            xs.append(log)

        xs = np.concatenate(xs, axis = 1)

        pos = minimum_curvature(
            src   = self.source,
            depth = xs[2],
            n     = xs[0],
            e     = xs[1],
            dls = self.dls,
        )
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

class radius_curvature(position_log):
    def __init__(self, src, depth, n, e):
        super().__init__(src, depth, n, e)

    def copy(self):
        l = radius_curvature(self.source, np.copy(self.depth), np.copy(self.northing), np.copy(self.easting))
        return l

class tan_method(position_log):
    def __init__(self, src, depth, n, e):
        super().__init__(src, depth, n, e)

    def copy(self):
        l = tan_method(self.source, np.copy(self.depth), np.copy(self.northing), np.copy(self.easting))
        return l
