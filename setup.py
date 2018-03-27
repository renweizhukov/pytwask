# -*- coding: utf-8 -*-

"""A setuptools-based setup module.

See:
https://github.com/renweizhukov/pytwask
"""

from setuptools import setup

setup(
    name='pytwask',
    packages=['pytwask'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    scripts = [
        './autopytwask.py',
    ]
)