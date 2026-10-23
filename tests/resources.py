# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower

import queuemo

hoverpower.setup(queuemo.ROOT)

RESOURCES = hoverpower.generated()

TODO = os.path.join(RESOURCES, 'todo')

EXAMPLE_JOB_ID = '8166109011'
EXAMPLE_JOB_PATH = os.path.join(TODO, EXAMPLE_JOB_ID)
EXAMPLE_PDF = os.path.join(EXAMPLE_JOB_PATH, EXAMPLE_JOB_ID)
