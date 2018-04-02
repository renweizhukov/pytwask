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
        'flask_debugtoolbar',
        'flask_login',
        'flask_moment',
        'flask_wtf',
        'pytwis'
    ],
    scripts = [
        './autopytwask.py',
    ]
)