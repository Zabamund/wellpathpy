# README

**this is Work in progress**


Contributors:
- [Robert Leckenby](https://github.com/Zabamund)
- [Brendon Hall](https://github.com/brendonhall)
- [Jørgen Kvalsvik](https://github.com/jokva)

## wellpathpy

This is a prototype library to import well deviations, calculate their TVD values
using a choice of methods and return them in one of several formats.


## Goal

To build a light package to load well deviations

## Objectives

- load well deviation in one of <n> formats:
    * meta data (header, rkb, dfe, rt)
    * md, incl, azi
    * mE, mN, depth
    * other ?,?,?
- interpolate survey using one of these methods:
    * minimum curvature method
    * radius of curvature method
    * tangential method
    * other ?
- calculate dog-leg severity
- calculate depth references using header data if available: MD, TVD, TVDSS
- return interpolated deviation in all <n> input formats and in all depth references if possible
- resample on regular steps
