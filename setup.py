#!/usr/bin/env python3

from setuptools import setup

long_description = """
To do
"""

setup(name='wellpathpy',
      description='Light package to load well deviations',
      long_description=long_description,
      author='Robert Leckenby, Brendon Hall, Jørgen Kvalsvik',
      author_email='fracgeol@gmail.com',
      url='https://github.com/Zabamund/wellpathpy',
      packages=['wellpathpy'],
      license='LGPL-3.0',
      platforms='any',
      install_requires=['numpy >=1.10', 'pandas', 'matplotlib'],
      setup_requires=['setuptools >=28', 'setuptools_scm', 'pytest-runner'],
      tests_require=['pytest'],
      use_scm_version=True,
      )
