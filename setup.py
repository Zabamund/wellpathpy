#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='wellpathpy',
      description='Light package to load well deviations',
      long_description=long_description,
      author='Robert Leckenby, Brendon Hall, Jørgen Kvalsvik',
      author_email='fracgeol@gmail.com',
      url='https://github.com/Zabamund/wellpathpy',
      packages=['wellpathpy'],
      license='LGPL-3.0',
      platforms='any',
      install_requires=['numpy >=1.10', 'pint'],
      setup_requires=['setuptools >=28', 'setuptools_scm', 'pytest-runner'],
      tests_require=['pytest', 'hypothesis'],
      use_scm_version=True,
      )
