# -*- coding: utf-8 -*-

"""A setuptools-based setup module.

See:
https://github.com/renweizhukov/pytwask
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pytwask',
    version='0.1.5',
    description='A twitter-toy-clone frontend using Python and Flask',
    long_description=long_description,
    # TODO: Replace url by the GitHub Pages.
    url='https://renweizhukov.github.io/pytwask',
    author='Wei Ren',
    author_email='renwei2004@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        ],
    keywords='flask twitter python3.6',
    packages=find_packages(exclude=['doc', 'tests']),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask_DebugToolbar',
        'Flask_Login',
        'Flask_Moment',
        'Flask_WTF',
        'WTForms',
        'itsdangerous',
        'pytwis',
        'setuptools',
    ],
    # This project depends on a module `pytwis` only available 
    # in Python 3.6 and later.
    python_requires='>=3.6',
    scripts = [
        './autopytwask.py',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/renweizhukov/pytwask/issues',
        # TODO: Replace documentation url by the GitHub Pages.
        'Documentation': 'https://renweizhukov.github.io/pytwask',
        'Source': 'https://github.com/renweizhukov/pytwask',
        },
    )