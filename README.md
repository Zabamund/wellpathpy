# README

[wellpathpy/master](https://github.com/Zabamund/wellpathpy/tree/master):[![Build Status](https://travis-ci.com/Zabamund/wellpathpy.svg?branch=master)](https://travis-ci.com/Zabamund/wellpathpy)
[wellpathpy/api_models](https://github.com/Zabamund/wellpathpy/tree/api_models):[![Build Status](https://travis-ci.com/Zabamund/wellpathpy.svg?branch=api_models)](https://travis-ci.com/Zabamund/wellpathpy)

## Contributors:

- [Robert Leckenby](https://github.com/Zabamund)
- [Brendon Hall](https://github.com/brendonhall)
- [Jørgen Kvalsvik](https://github.com/jokva)

## Introduction

`wellpathpy` is a LGPL-3.0 licensed library to import well deviations in (md, inc, azi) format, calculate their TVD values using a choice of methods and return them as positional logs in (tvd, northing, easting) format.

## Features

- load well deviation in (md, inc, azi) format:
    * meta data (header, rkb, dfe, rt)
    * md, incl, azi
- interpolate survey using one of these methods:
    * minimum curvature method
    * radius of curvature method
    * tangential method
- calculate dog-leg severity
- calculate depth references using header data if available: MD, TVD, TVDSS
- return interpolated deviation in (tvd, northing, easting) format
- move surface location to (0, 0, 0) or to (kb, mE, mN)
- convert to tvdss based on kb elevation
- resample deviation on regular steps

## Installation

**This is work in progress**

From [pypi](https://pypi.org/project/wellpathpy/) with:

`pip install wellpathpy`

## Requirements

- [pandas](https://pandas.pydata.org/) version 0.24.2 or greater
- [numpy](https://numpy.org/) version 1.16.2 or greater
- [scipy](https://www.scipy.org/) version 1.2.1 or greater
- [pytest](https://pytest.org/) version 4.3.1 or greater
- [pint](https://github.com/hgrecco/pint) version 0.9 or greater

## Tutorials

Currently work-in-progress in [branch:api_models](https://github.com/Zabamund/wellpathpy/tree/api_models).

## Contributing

We welcome all kinds of contributions, including code, bug reports, issues, feature requests, and documentation. The preferred way of submitting a contribution is to either make an issue on github or by forking the project on github and making a pull request.

## History

wellpathpy started as a community project during the [May 2019 Transform event](https://agilescientific.com/blog/2019/5/18/transform-happened).