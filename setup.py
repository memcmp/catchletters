#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    'cocos2d'
]

setup(
    name='catchletters',
    packages=['catchletters'],
    entry_points={
        'console_scripts': [
            'catchletters = catchletters.main:main'
        ]
    },
    install_requires=requirements
)
