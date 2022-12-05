#!/usr/bin/env python
#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

PACKAGES = [
    'queuemo',
    'queuemo.cli',
    'queuemo.recipes',
    'queuemo.recipes.fastview',
    'queuemo.recipes.publish',
    'queuemo.recipes.result',
    'queuemo.recipes.validation',
    'queuemo.runtime',
    'queuemo.worker',
]
ENTRY_POINTS = dict(console_scripts=[
    'queuemo = queuemo.cli.main:main',
    'queuemo_single = queuemo.cli.single:main',
    'queuemo_state = queuemo.cli.state:main',
])

if __name__ == "__main__":
    utila.install(__file__)
