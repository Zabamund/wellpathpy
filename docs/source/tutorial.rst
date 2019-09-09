*******************
Wellpathpy tutorial
*******************

This document aims to provide a sample workthrough using wellpathpy showing:

- `Abbreviations`_
- `Imports`_
- `Loading a deviation`_
- `Loading the well header`_
- `Converting units`_
- `Converting deviation surveys to positional logs`_
- `Well location and tvdss`_
- `Exporting results`_

Abbreviations
#############

=============== ==========================================================================
m               metres
ft              feet
md              measured depth
inc             inclination
azi             azimuth
tvd             true vertical depth
east_offset     horizontal distance away from wellhead towards the east
north_offset    horizontal distance away from wellhead towards the north
tvdss           true vertical depth subsea
mE              horizontal distance in meters away from surface location towards the east
mN              horizontal distance in meters away from surface location towards the north
=============== ==========================================================================

Imports
#######

In this tutorial, we will alias wellpathpy as wp:

.. code-block:: python

   import wellpathpy as wp

Loading a deviation
###################

Wellpathpy provides a fairly simple loading function for reading a deviation
survey from CSV.

Loading a deviation from CSV
****************************

A valid input file must be a CSV file containing the columns: md, inc, azi in that order, as shown in this example:

.. code-block:: python

    md,inc,azi
    0,0,244
    10,11,220
    50,43,254
    150,78.5,254
    252.5,90,359.9

- column headers are **required**
- md must increase monotonically
- as inc and azi cannot be distinguished numerically it is the user's responsibility to ensure the data are passed in in this order
- inc must be in range 0-180 (to allow for horizontal wells to climb)
- azi must be in range 0-360

You can then load them into wellpathpy using:

.. code-block:: python

   md, inc, azi = wp.read_csv(fname)

**Notes**:

Some simple sanity checks are performed to reject bad CSVs. ``wp.read_csv`` supports all options ``pd.read_csv`` supports. Only those columns named md, inc, azi will be read.

If the deviation survey is not in CSV, is generated a different place in your
program, or is from some other source, wellpathpy is still useful. If you
provide three ``np.ndarray`` md, inc, and azi, the rest of wellpathpy works fine.

Observe that the same basic requirements still apply:

- md, inc and azi have the same shape
- md increases monotonically
- inc is in range 0-180
- azi is in range 0-360

Loading the well header
#######################

To make sense of the deviation position, wellpathpy supports reading a survey
header from json file. The header requires the following keys:

.. code-block:: json

    {
    "datum": "kb",
    "elevation_units": "m",
    "elevation": 100.0,
    "surface_coordinates_units": "m",
    "surface_easting": 1000.0,
    "surface_northing": 2000.0
    }

.. code-block:: python

    header = wp.read_header_json(fname)

**Notes**:

This function is provided for convenience - wellpathpy does not care about the
source of this data.

Converting units
################

Wellpathpy does not implicitly convert between unit systems for you, but
assumes all units are consistent. In practice, that's not always the case, and
wellpathpy provides a simple function to convert data between unit systems.

That means wellpathpy assumes the provided date are in SI units and degrees:

    ===================  =================================
    md                   meters
    inc                  degrees
    azi                  degrees
    elevation            meters above mean sea level
    surface_easting      meters east of reference point
    surface_northing     meters north of reference point
    ===================  =================================

**Notes:**

- The units for elevation, surface_northing and surface_easting must be the same as the md units before any md->tvd calculations are run, otherwise you will get inconsistent results.
- inc and azi must always be passed as degrees, otherwise erroneous results will be returned.

Conversion API
**************

To convert between unit systems, you can use the unit_convert function:

.. code-block:: python

    md               = wp.unit_convert(md, src='ft', dst='m')
    elevation        = wp.unit_convert(header['elevation'],
                                   src=header['elevation_units'], dst='m')
    surface_easting  = wp.unit_convert(header['surface_easting'],
                                    src=header['surface_coordinates_units'],
                                    dst='m')
    surface_northing = wp.unit_convert(header['surface_northing'],
                                    src=header['surface_coordinates_units'],
                                    dst='m')

Observe that the elevation and coordinate units are never explicitly read in
the program, they're only passed to unit_convert.

The `pint <https://github.com/hgrecco/pint>`_ library drives the unit
conversion. If you require units not already known to pint, you can pass your
own `unit registry <https://pint.readthedocs.io/en/latest/defining.html#programmatically>`_.
Consider the need of converting a bizarre devation survey in
`ell <https://en.wikipedia.org/wiki/Ell>`_ to meters:

.. code-block:: python

    import pint
    ureg             = pint.UnitRegistry()
    ureg.define('ell = 0.6275 * meter = ell')
    result           = wp.unit_convert(data, src='ell', dst='m', ureg=ureg)

Converting deviation surveys to positional logs
###############################################

wellpathpy provides the following methods to convert **deviation surveys** md, inc, azi into **positional logs** tvd, northing, easting:

Recommended methods
*******************

These methods are most commonly used in drilling operations and are recommended for most cases:

- **minimum curvature method** : ``wp.mininum_curvature``
    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points.
    This curve is
    smoothed by use of the ratio factor defined by the tortuosity or dogleg
    of the wellpath.
    This method returns a dogleg severity calculated for a given course_length.
- **radius of curvature method** : ``wp.radius_curvature``
    Calculate TVD using radius or curvature method.
    **Caution**: this will yield unreliable results when data are closely spaced
    or when the borehole is straight but deviated.
    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points.

Comparison methods
******************

These methods might be used for comparison to the recommended methods:

- **average tan method** : ``wp.average_tan``
    Calculate TVD using average tangential method.
    This method averages the inclination and azimuth at the top and
    bottom of the survey interval before taking their sine and cosine,
    this average angle is used to estimate tvd.
- **balanced tan method** : ``wp.balanced_tan``
    Calculate TVD using balanced tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the top and bottom of the survey interval before averaging them,
    this average angle is used to estimate tvd.
    This will provide a smoother curve than the ave_tan method but requires
    closely spaced survey stations to avoid errors.

Not recommended methods
***********************

These methods are provided for completeness and in case a comparison must be made to an existing survey using these methods, but they are *not recommended*:

- **high tan method** : ``wp.high_tan``
    Calculate TVD using high tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the bottom of the survey interval to estimate tvd.
    This method is **not recommended** as it can make gross tvd and offset
    errors in typical deviated wells.
- **low tan method** : ``wp.low_tan``
    Calculate TVD using low tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the top of the survey interval to estimate tvd.
    This method is **not recommended** as it can make gross tvd and offset
    errors in typical deviated wells.

Usage
*****

In order to use any of these functions, you can run the following code once you've imported your deviation and header and done any unit conversion required as described above:

Recommended usage:

.. code-block:: python

    tvd, northing, easting, dls = wp.mininum_curvature(md, inc, azi, course_length=30)
    tvd, northing, easting      = wp.radius_curvature(md, inc, azi)

Well location and tvdss
#######################

The methods above are not aware of surface location or datum elevation. If you want to move the positional log tvd, northing, easting to a given surface location, to 0,0 coordinates, or shift the tvd to tvdss, you can use the following functions:

- to shift a positional log to a wellhead location

.. code-block:: python

    tvd, new_northing, new_easting = wp.loc_to_wellhead(tvd, northing, easting, surface_northing, surface_easting)

- to shift a positional log to a 0,0 coordinate location

.. code-block:: python

    tvd, new_northing, new_easting = wp.loc_to_zero(tvd, northing, easting, surface_northing, surface_easting)

- to shift a positional log to tvdss

.. code-block:: python

    new_tvdss, northing, easting   = wp.loc_to_tvdss(tvd, northing, easting, datum_elevation)

If you have a header loaded as shown in the `Loading the well header`_ section, you can use that object to access the required properties with:

.. code-block:: python

    surface_northing = header['surface_northing']
    surface_easting  = header['surface_easting']
    datum_elevation  = header['datum_elevation']

**Notes:**

Ensure you have consistent units, and use `Converting units`_ if required to ensure consistency.

Exporting results
#################

Once you have converted your deviation survey to a positional logs, you can write the results to a CSV file with:

- for a deviation survey:

.. code-block:: python

    wp.deviation_to_csv(fname, md, inc, azi)

- for a positional log:

.. code-block:: python

    wp.position_to_csv(fname, depth, northing, easting)

This is a pretty straight-forward function convenient CSV writing. If you need
more control, or more sophisticated output, you must implement your own writer.
