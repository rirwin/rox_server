#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='rox_server',
    packages=find_packages(exclude=['tests*']),
    setup_requires=['setuptools']
)
