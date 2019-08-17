*******************
Wellpathpy tutorial
*******************

This document aims to provide a sample workthrough using ``wellpathpy`` showing:

- `Abbreviations`_ used in wellpathpy
- `Imports`_
- `Loading a deviation`_
- `Loading the well header`_
- `Converting units`_
- `Converting deviation surveys to positional logs`_
- `Resample a deviation survey or positional log`_
- `Well location and tvdss`_
- `Exporting results`_

Abbreviations
#############

- m: metres
- ft: feet
- md: measured depth
- inc: inclination
- azi: azimuth
- tvd: true vertical depth
- east_offset: horizontal distance away from wellhead towards the east
- north_offset: horizontal distance away from wellhead towards the north
- tvdss: true vertical depth subsea
- mE: horizontal distance in meters away from surface location towards the east
- mN: horizontal distance in meters away from surface location towards the north

Imports
#######

wellpathpy depends on `numpy <https://www.numpy.org/>`_, `pandas <https://pandas.pydata.org/>`_ and `pint <https://github.com/hgrecco/pint>`_.
In this tutorial, we will alias wellpathpy as wp:

.. code-block:: python

   import wellpathpy as wp

Loading a deviation
###################

There are two main ways of loading a deviation for use in wellpathpy, from a CSV file or within Python from a ``pd.DataFrame`` or a ``np.ndarray``:

1. Loading a deviation from `*.csv`
***********************************

A valid input file must be a `*.csv` file containing the columns: ('md', 'inc', 'azi') in that order, as shown in this example:

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

The ``wp.read_csv`` function reads a deviation survey from a CSV file. The columns must be named md, inc, azi, and md must be strictly increasing. Some simple sanity checks are performed to reject bad CSVs. ``wp.read_csv`` supports all options ``pd.read_csv`` supports. Only those columns named md, inc, azi will be read.

2. Loading a deviation from a `pd.DataFrame` or a `np.ndarray`
**************************************************************

In order to use wellpathpy, you will need three ``np.ndarray`` objects: md, inc and azi.
If you create these with pandas or NumPy you can still use wellpathpy as long as they fit the following criteria:

- md, inc and azi have the same ``.shape`` attribute
- md increases monotonically
- inc is in range 0-180
- azi is in range 0-360

Loading the well header
#######################

Assuming the well header information in a \*.json file with this format and keys:

.. code-block:: json

    {
    "datum": "kb",
    "elevation_units": "m",
    "elevation": 100.0,
    "surface_coordinates_units": "m",
    "surface_easting": 1000.0,
    "surface_northing": 2000.0
    }

we can load it with:

.. code-block:: python

    header = wp.read_header_json(fname)

**Notes**:

You can also create a Python `dict` with the same keys of course.

Converting units
################

By default, no unit conversions are run by wellpathpy, you therefore have the following options:

1. Import your deviations and headers in consistent SI units where:
    - md: meters
    - inc: degrees
    - azi: degrees
    - elevation: meters above mean sea level
    - surface_easting: meters east of reference point
    - surface_northing: meters north of reference point

2. Import deviations and headers in other units (e.g. feet) and convert to SI units:
    - md: feet
    - inc: degrees
    - azi: degrees
    - elevation: feet above mean sea level
    - surface_easting: feet east of reference point
    - surface_northing: feet north of reference point

**Notes:**

- The units for elevation, surface_northing and surface_easting must be the same as the md units before any md->tvd calculations are run, otherwise you will get inconsistent results.
- inc and azi must always be passed as degrees, otherwise erroneous results will be returned.

Conversion API
**************

In order to convert md, elevation, surface_easting or surface_northing from ft to m where elevation_units and surface_coordinates_units are in ft for example, run:

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

We depend on `pint <https://github.com/hgrecco/pint>`_ for the unit conversions. This means that you can add in your own units to the `unit registry <https://pint.readthedocs.io/en/latest/defining.html#programmatically>`_ and then convert a quantity data from a unit `ell <https://en.wikipedia.org/wiki/Ell>`_ for example to meters with the example below:

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

- ``wp.mininum_curvature`` **minimum curvature method**
    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points.
    This curve is
    smoothed by use of the ratio factor defined by the tortuosity or dogleg
    of the wellpath.
    This method returns a dogleg severity calculated for a given course_length.
- ``wp.radius_curvature`` **radius of curvature method**
    Calculate TVD using radius or curvature method.
    **Caution**: this will yield unreliable results when data are closely spaced
    or when the borehole is straight but deviated.
    This method uses angles from upper and lower end of survey interval to
    calculate a curve that passes through both survey points.

Comparison methods
******************

These methods might be used for comparison to the recommended methods:

- ``wp.average_tan`` **average tan method**
    Calculate TVD using average tangential method.
    This method averages the inclination and azimuth at the top and
    bottom of the survey interval before taking their sine and cosine,
    this average angle is used to estimate tvd.
- ``wp.balanced_tan`` **balanced tan method**
    Calculate TVD using balanced tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the top and bottom of the survey interval before averaging them,
    this average angle is used to estimate tvd.
    This will provide a smoother curve than the ave_tan method but requires
    closely spaced survey stations to avoid errors.

Not recommended methods
***********************

These methods are provided for completeness and in case a comparison must be made to an existing survey using these methods, but they are *not recommended*:

- ``wp.high_tan`` **high tan method**
    Calculate TVD using high tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the bottom of the survey interval to estimate tvd.
    This method is **not recommended** as it can make gross tvd and offset
    errors in typical deviated wells.
- ``wp.low_tan`` **low tan method**
    Calculate TVD using low tangential method.
    This method takes the sines and cosines of the inclination and azimuth
    at the top of the survey interval to estimate tvd.
    This method is **not recommended** as it can make gross tvd and offset
    errors in typical deviated wells.

Usage
*****

In order to use any of these functions, you can run the following code once you've imported your deviation (`Loading a deviation`_) and header (`Loading the well header`_) and done any unit conversion (`Converting units`_) required as described above:

Recommended usage:

.. code-block:: python

    tvd, northing, easting, dls = wp.mininum_curvature(md, inc, azi, course_length=30)
    tvd, northing, easting      = wp.radius_curvature(md, inc, azi)

Backup usage:

.. code-block:: python

    tvd, northing, easting = wp.average_tan(md, inc, azi)
    tvd, northing, easting = wp.balanced_tan(md, inc, azi)

Not recommended:

.. code-block:: python

    tvd, northing, easting = wp.high_tan(md, inc, azi)
    tvd, northing, easting = wp.low_tan(md, inc, azi)

Resample a deviation survey or positional log
#############################################

As deviation surveys are often not sampled at regular intervals, wellpathpy allows you to interpolate either a deviation survey or a positional log onto a given ``md_step`` or ``tvd_step``.

Usage
*****

- Resampling a deviation survey:

.. code-block:: python

    new_md, new_inc, new_azi           = resample_deviation(md, inc, azi, md_step=1)

- Resampling a positional log:

.. code-block:: python

    new_tvd, new_easting, new_northing = resample_position(tvd, easting, northing, tvd_step=1)

**Notes:**

- ``wp.resample_deviation()`` should not be used before md -> tvd conversions. Rather, convert your deviation survey to a positional log first, and then resample them onto a new `tvd_step` if needed.

- ``wp.resample_position()`` requires that the tvd values must be strictly increasing, i.e. this method will **not work** on horizontal wells, use ``wp.resample_deviation()`` for those wells. In order to interpolate only a section of a positional log, you can slice into it and pass a monotonically increasing tvd section only.

- input arrays must not contain NaN values.

Well location and tvdss
#######################

The methods above are not aware of surface location of datum elevation. If you want to move the positional log tvd, northing, easting to a given surface location, to 0,0 coordinates, or shift the tvd to tvdss, you can use the following functions:

- to shift a positional log to a wellhead location

.. code-block:: python

    tvd, new_northing, new_easting = wp.loc_to_wellhead(tvd, northing, easting, surface_northing, surface_easting)

- to shift a positional log to a 0,0 coordinate location

.. code-block:: python

    tvd, new_northing, new_easting = wp.loc_to_zero(tvd, northing, easting, surface_northing, surface_easting)

- to shift a positional log to tvdss

.. code-block:: python

    new_tvdss, northing, easting = def loc_to_tvdss(tvd, northing, easting, datum_elevation)

If you have a header loaded as shown in the `Loading the well header`_ section, you can use that object to access the required properties with:

.. code-block:: python

    surface_northing = header['surface_northing']
    surface_easting  = header['surface_easting']
    datum_elevation  = header['datum_elevation']

**Notes:**

Ensure you have consistent units, and use `Converting units`_ if required to ensure consistency.

Exporting results
#################

Once you have converted your deviation survey to a positional logs, you can write the results to a \*.csv file with:

- for a deviation survey:

.. code-block:: python

    wp.deviation_to_csv(fname, md, inc, azi)

- for a positional log:

.. code-block:: python

    wp.position_to_csv(fname, depth, northing, easting)

where:

fname: file path or object the CSV will be written to

These functions rely on ``pandas.DataFrame.to_csv`` and are provided as a convenience only.