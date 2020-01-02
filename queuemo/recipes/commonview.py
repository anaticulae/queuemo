# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import join

from queuemo.recipes import COMMON_VIEW_WORK
from queuemo.recipes import GROUPME
from queuemo.recipes import RAWMAKER_OUTPUT
from queuemo.recipes import copy
from queuemo.recipes import feedback
from queuemo.recipes import publish
from queuemo.recipes import words


def require():
    'docsplit'


def before(rawspace: str):
    # Words?
    copy(rawspace, GROUPME, COMMON_VIEW_WORK)
    copy(rawspace, RAWMAKER_OUTPUT, COMMON_VIEW_WORK)

    words(rawspace, COMMON_VIEW_WORK, COMMON_VIEW_WORK)


def run(rawspace: str):
    feedback(rawspace, COMMON_VIEW_WORK, COMMON_VIEW_WORK)


def after(rawspace: str):
    viewout = join(COMMON_VIEW_WORK, 'feedback__view_result.html')
    publish(rawspace, viewout, 'view/landing/overview')
