#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


def parse_requirements():
    with open('requirements.txt', 'r') as f:
        return ['{2} @ {0}'.format(*r.partition('#egg=')) if '#egg=' in r else r for r in f.read().splitlines()]


# The README.md will be used as the content for the PyPi package details page on the Python Package Index.
with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name='polyswarm-transaction',
    version='0.1.0',
    description='Library for building & signing transactions for the PolySwarmd sidechain',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='PolySwarm Developers',
    author_email='info@polyswarm.io',
    url='https://github.com/polyswarm/polyswarm-transaction',
    license='MIT',
    python_requires='>=3.6,<4',
    install_requires=parse_requirements(),
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src/'},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
