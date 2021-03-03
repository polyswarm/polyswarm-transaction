#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

# The README.md will be used as the content for the PyPi package details page on the Python Package Index.
with open("README.md", "r") as readme:
    long_description = readme.read()


def parse_requirements():
    with open('requirements.txt', 'r') as f:
        reqs = []
        for r in f.read().splitlines():
            if r.startswith('#'):
                pass
            elif '#egg=' in r:
                reqs.append('{2} @ {0}'.format(*r.partition('#egg=')))
            else:
                reqs.append(r)


setup(
    name='polyswarm-transaction',
    version='0.4.1',
    description='Library for building & signing transactions for the PolySwarm sidechain',
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
    package_dir={'': 'src'},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
