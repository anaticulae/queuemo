#!/usr/bin/env python
#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from os.path import dirname
from os.path import join
from re import search

from setuptools import setup

ROOT = dirname(__file__)
with open(join(ROOT, 'README.md'), 'rt', encoding='utf8') as fp:
    README = fp.read()

with open(join(ROOT, 'queuemo/__init__.py'), 'rt', encoding='utf8') as fp:
    VERSION = search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(join(ROOT, 'requirements.txt'), mode='rt', encoding='utf8') as fp:
    INSTALL_REQUIRES = [
        line for line in fp.readlines() if line and '#' not in line
    ]

DATA_FILES = [
    ('.', [
        'CHANGELOG.md',
        'README.md',
        'requirements.txt',
    ]),
    ('config', [
        'config/decider_fonts_config__ugly_fonts.yaml',
    ]),
]

if __name__ == "__main__":
    setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        data_files=DATA_FILES,
        description='queuemo',
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        long_description=README,
        name='queuemo',
        platforms='any',
        url='https://dev.package.checkitweg.de/queuemo',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        entry_points={
            'console_scripts': ['queuemo = queuemo.cli:main'],
        },
        packages=[
            'queuemo',
            'queuemo.recipes',
            'queuemo.recipes.decider',
            'queuemo.recipes.fastview',
            'queuemo.recipes.publish',
            'queuemo.recipes.result',
            'queuemo.recipes.validation',
            'queuemo.runtime',
            'queuemo.worker',
        ],
    )
