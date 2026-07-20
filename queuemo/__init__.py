#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

import queuemo.__patch__
from queuemo.runtime.api import RecipeIO
from queuemo.runtime.scheduler import isrequired
from queuemo.runtime.scheduler import required

__version__ = importlib.metadata.version('queuemo')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'queuemo'

INTERACTIVE = False  # if True, pause on every scheduler step
