# README

[wellpathpy/master](https://github.com/Zabamund/wellpathpy/tree/master):
[![Build Status](https://travis-ci.com/Zabamund/wellpathpy.svg?branch=master)](https://travis-ci.com/Zabamund/wellpathpy)

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
- calculate position log survey using one of these methods:
    * minimum curvature method
    * radius of curvature method
    * tangential methods
- calculate dog-leg severity from minimum curvature
- calculate depth references using header data if available: MD, TVD, TVDSS
- return interpolated deviation in (tvd, northing, easting) format
- move surface location to (0, 0, 0) or to (kb, mE, mN)
- convert to tvdss based on kb elevation
- resample deviation on regular steps with minimum curvature only

## Installation

**This is work in progress**

From [pypi](https://pypi.org/project/wellpathpy/) with:

`pip install wellpathpy`

## Requirements

- [numpy](https://numpy.org/) version 1.16.2 or greater
- [pint](https://github.com/hgrecco/pint) version 0.9 or greater

## Tutorials

A tutorial is available on [wellpathpy.readthedocs.io](https://wellpathpy.readthedocs.io/en/latest/tutorial.html)

## Contributing

We welcome all kinds of contributions, including code, bug reports, issues, feature requests, and documentation. The preferred way of submitting a contribution is to either make an issue on github or by forking the project on github and making a pull request.

## History

wellpathpy started as a community project during the [May 2019 Transform event](https://agilescientific.com/blog/2019/5/18/transform-happened).