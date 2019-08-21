import os
import numpy as np

class SurveyError(Exception):
    pass

class SurveyWarning(UserWarning):
    pass

def modulus(theta, modby):
    """
    Calculate the positive cyclic modulus of theta by modby.
    """
    is_scalar = np.ndim(theta) == 0
    theta = np.atleast_1d(theta)
    
    k = (theta / modby).astype(int)
    theta -= k * modby
    theta[theta < 0.0] += modby
    return theta[0] if is_scalar else theta

def quantize(x, fraction=0.5):
    """
    Round a number, or list of numbers, to the closest fraction.
    >>> quantize(1.3, fraction=0.5)
    1.5
    >>> quantize(2.6, fraction=0.5)
    2.5
    >>> quantize(3.0, fraction=0.5)
    3.0
    >>> quantize(4.1, fraction=0.5)
    4.0
    >>> quantize([1.3, 2.6, 3.0 ,4.1], fraction=0.5)
    [1.5, 2.5, 3.0, 4.0]
    """
    
    is_scalar = np.ndim(x) == 0
    x = np.atleast_1d(x)
    
    div = 1.0 / fraction
    qnt = np.round(x * div) / div
    return qnt[0] if is_scalar else qnt

def toUnitDir(degINC, degAZ):
    """
    Convert spherical coordinates to cubic coordinates (NEV), a unit length direction vector
    in a right handed coordinate system.
    """
    dim_inc = np.ndim(degINC)
    is_scalar = dim_inc == 0
    degINC = np.atleast_1d(degINC)
    degAZ = np.atleast_1d(degAZ)
    
    inc = np.deg2rad(degINC)
    az = np.deg2rad(degAZ)
    deltaN = np.sin(inc) * np.cos(az)
    deltaE = np.sin(inc) * np.sin(az)
    deltaV = np.cos(inc)

    nev = np.column_stack((deltaN, deltaE, deltaV))
    return nev[0] if is_scalar else nev

def toSpherical(unit_t):
    """
    Convert a unit direction vector in NEV coordinates to a tuple of Inclination and Azimuth.
    """
    is_1d = np.ndim(unit_t) == 1
    unit_t = np.atleast_2d(unit_t)
    
    inc = np.arctan2(np.sqrt(unit_t[:,0] * unit_t[:,0] + unit_t[:,1] * unit_t[:,1]), unit_t[:,2])
    az = np.arctan2(unit_t[:,1], unit_t[:,0])
    # return a result for az such that az is [0.0, 360.0)
    az[az < 0.0] += 2.0 * np.pi
    ia = np.column_stack((np.rad2deg(inc), np.rad2deg(az)))
    return ia[0] if is_1d else ia

def slerp(t, u, v, theta=None):
    """
    Spherical linear interpolation.
    Returns a unit vector a fraction, t, between unit vectors u and v.
    t: a float or an array of floats to interpolate.
    u and v: are unit vectors.
    theta: the angle between u and v. If none then the angle is calculated.
    """
    def _sin_over_x(x):
        """
        Numerically stable sin_over_x function.
        """
        mask = 1.0 + (x * x) == 1.0
        x[mask] = 1.0
        x[~mask] = np.sin(x[~mask]) / x[~mask]
        return x
    
    is_scalar = np.ndim(t) == 0
    t = np.atleast_1d(t)[:,None]
    if theta is None:
        theta = 2.0 * np.arctan(np.linalg.norm(v - u) / np.linalg.norm(u + v))
    
    q = 1.0 - t
    d = _sin_over_x(np.atleast_1d(theta))[0]
    l = (_sin_over_x(q * theta) / d) * (q * u)
    r = (_sin_over_x(t * theta) / d) * (t * v)
    w = l + r
    
    return w[0] if is_scalar else w

def S_and_T_survey():
    """
    The test survey from Compendium One.
    """
    P1 = np.array([40.00, 40.00, 700.00]) # position at start (tie-in)
    srv = np.array([[702.55, 5.50, 45.00], [1964.57, 29.75, 77.05], [5086.35, 29.75, 77.05], [9901.68, 120.00, 285.00]])
    return srv, P1

def arc2chord(t1, t2, arclen):
    """
    Calculates the relative vector between two survey stations,
    given tangents at the ends of the arc and the arc length between
    the tangents.
    Assumes survey values are correct
    and if arrays of values, the arrays are all the same length.
    """
    is_scalar = np.ndim(arclen) == 0
    arclen = np.atleast_1d(arclen)
    cnt = len(arclen)
    t1 = np.atleast_2d(t1)
    t1 = np.atleast_2d(t1)
    
    t_add = t1 + t2 # add the tangent vectors; a vector that points to the end of the arc from the start
    lsqrd_t_add = np.einsum('ij,ij->i', t_add, t_add) # the length squared of the vector sum... same as: np.sum(t12*t12, axis=1)
    anti_parallel = lsqrd_t_add == 0 # test for anti-parallel tangent vectors, the singuar case
    lsqrd_t_add[anti_parallel] = 1.0 # set so we prevents div-by-zero when unitizing the direction vector
    len_t_add = np.sqrt(lsqrd_t_add) # the length of the addition vector
    norm_t_add = np.divide(t_add, len_t_add[:,None]) # normalized the addition vector to unit vector point to the end of the arc
    
    t_sub = t2 - t1 # subtract the tangent vectors; the chord of on a unit circle
    lsqrd_t_sub = np.einsum('ij,ij->i', t_sub, t_sub) # the length squared of the vector subtraction
    len_t_sub = np.sqrt(lsqrd_t_sub) # the length of the subtraction vector
    
    alpha = 2.0 * np.arctan(np.divide(len_t_sub, len_t_add)) # the unoriented angle between the tangent vectors; the arc length on a unit circle
    
    geom_test = len_t_sub < alpha # do the degenerate circle geometry test, the straight hole test
    arc_2_chord = np.ones(cnt) # if degenerte, we are at unity
    arc_2_chord[geom_test] = np.divide(len_t_sub[geom_test], alpha[geom_test]) # where not unity, calc ratio
    
    relative_pos = (arclen * arc_2_chord)[:,None] * norm_t_add # arc-2-chord. For robust numeric evaluation the order of operations here are important
    relative_pos[anti_parallel] = np.array([np.nan, np.nan, np.nan]) # set any singuar cases to nan because they have vanished
    
    return (relative_pos[0], alpha[0]) if is_scalar else (relative_pos, alpha)

def position_log(survey, tie_in, report_raw=False):
    """
    Calculate a position log from a deviation survey and tie-in location
    """
    md = survey[:,0]
    if np.all(md[:1] > md[:-1]):
        raise SurveyError('All measured depths must be strictly increasing.')
        
    arclen = md[1:] - md[:-1]
    if np.any(arclen <= 0.0):
        raise SurveyError('All arclens must be GT 0.')
    
    inc = modulus(survey[:,1], 180.0)
    if not np.all(inc == survey[:,1]):
        raise SurveyWarning('One or more inclination values are not GTEQ 0 and LT 180.')
    
    az = modulus(survey[:,2], 360.0)
    if not np.all(az == survey[:,2]):
        raise SurveyWarning('One or more azimuth values are not GTEQ 0 and LT 360.')
    
    tangents = toUnitDir(inc, az)
    rela_pos, alpha = arc2chord(tangents[:-1], tangents[1:], arclen)
    
    pos = tie_in + np.cumsum(rela_pos, axis=0)
    pos = np.concatenate(([tie_in], pos), axis=0)
    
    if report_raw:
        angle = np.concatenate(([0.0], alpha))
        k = np.concatenate(([0.0], np.divide(alpha, arclen)))
        return np.column_stack((md, tangents, pos, angle, k))
    else:
        dog_leg = np.concatenate(([0.0], np.divide((18000.0 * np.divide(alpha, np.pi)), arclen)))
        return np.column_stack((md, inc, az, pos, dog_leg))

def inslerpolate(survey, tie_in, step=None, report_raw=False):
    """
    Interpolate a deviation survey via slerp.
    survey: a list deviation surveys.
    tie_in: the 3D position of the first survey in survey.
    step: the step size to interpolate the survey at, or a list of depths to interpolate.
    If step is None, just calculate the survey.
    report_raw: how to report the resulting position.
    """
    if step is None:
        return position_log(survey, tie_in, report_raw=report_raw)
    pos_log = position_log(survey, tie_in, report_raw=True)

    mds = pos_log[:,0]
    tangents = pos_log[:,1:4]
    tie_ins = pos_log[:,4:7]
    angles = pos_log[:,7]
    
    if np.ndim(step) == 0:
        quant_ends = quantize([mds[0], mds[-1]], step)
        interp_depths = np.arange(quant_ends[0], quant_ends[1] + step, step)
    else:
        interp_depths = np.atleast_1d(step)
    
    interp_pos_logs = []
    
    segment_cnt = len(mds) - 1
    for i in np.arange(segment_cnt):
        md1, md2 = mds[i:i+2]
        v0, v1 = tangents[i:i+2]
        
        if (i < segment_cnt  - 1):
            mds_i = interp_depths[(interp_depths >= md1) & (interp_depths < md2)]
        else:
            mds_i = interp_depths[(interp_depths >= md1) & (interp_depths <= md2)]
            
        if len(mds_i) == 0:
            continue
            
        strip_head = mds_i[0] != md1
        if strip_head:
            strip_head = True
            mds_i = np.concatenate([[md1], mds_i])
        strip_tail = mds_i[-1] != md2
        if strip_tail:
            strip_tail = True
            mds_i = np.concatenate([mds_i, [md2]])
    
        t = (mds_i - md1) / (md2 - md1)
        ang = angles[i+1]
        v_i = slerp(t, v0, v1, ang)
        inc_az_i = toSpherical(v_i)
        srv_i = np.column_stack((mds_i, inc_az_i))
        tie_in_i = tie_ins[i]
        pos_log_i = position_log(srv_i, tie_in_i, report_raw=report_raw)
        
        if strip_head:
            pos_log_i = pos_log_i[1:]
        if strip_tail:
            pos_log_i = pos_log_i[:-1]
        interp_pos_logs.append(pos_log_i)
        
    return interp_pos_logs if len(interp_pos_logs) == 0 else np.concatenate(interp_pos_logs, axis=0)

def project(survey, tie_in, to_md, curvature=None, report_raw=False):
    """
    Project a deviation survey to a measured depth beyond the last survey station.
    Returns a deviation survey with the projected survey appended to the end.
    If curvature is None, the curvature from the last arc of the survey is used.
    """
    survey = np.asarray(survey)
    pos_log = position_log(survey, tie_in, report_raw=True)[-2:] # grab the last two surveys
    
    mds = pos_log[:,0]
    tangents = pos_log[:,1:4]
    angles = pos_log[:,7]
    
    if curvature is None:
        curvature = angles[1] / (mds[1] - mds[0]) # alpha / course_length
    
    if curvature <= 0: # straight hole
        sta_proj = np.concatenate([[to_md], toSpherical(tangents[1])])
        srv_plus = np.concatenate([survey, [sta_proj]], axis=0)
        return position_log(srv_plus, tie_in, report_raw=report_raw)
    
    t = (to_md - mds[1]) / (mds[1] - mds[0])
    ang = curvature * (mds[1] - mds[0])
    v_i = slerp(t, tangents[0], tangents[1], ang)
    sta_proj = np.concatenate([[to_md], toSpherical(v_i)])
    srv_plus = np.concatenate([survey, [sta_proj]], axis=0)
    return position_log(srv_plus, tie_in, report_raw=report_raw)

def verticalSection(vs_azimuth):
    """
    Calculates the vertical section of point or set of survey positions.
    http://people.eecs.berkeley.edu/~wkahan/MathH110/Cross.pdf
    Paragraph 9: Applications of Cross-Products to Geometrical Problems, #2
    vs_azimuth: the azimuth, in degrees, of the vertical section.
    """
    def _pee_cross(p):
        """
        http://people.eecs.berkeley.edu/~wkahan/MathH110/Cross.pdf
        p: a column vector.
        """
        return np.matrix([[0.0, -p[2], p[1]], [p[2], 0.0, -p[0]], [-p[1], p[0], 0.0]])
    
    az = toUnitDir(90.0, vs_azimuth)
    #u = np.matrix([0.0, 0.0, 0.0]).T # we don't need this as u is always the origin
    v = np.matrix([0.0, 0.0, 1.0]).T
    w = np.matrix(az).T # vector in horizontal plane pointing in the azimuth direction
    p = _pee_cross(v) * w
    pd = p.T * p
    
    def _f(y):
        """
        y: an array of 3D vectors, the position of the points, from the survey,
        relative to the origin of the survey.
        """
        z = y.T - p * p.T * y.T / pd # for the case of VS this in most cases will probably be more stable 
        z = np.asarray(z.T)
        z[:,2] = 0.0
        return np.dot(z, az)
    return _f
