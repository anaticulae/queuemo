# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from queuemo.recipes import FEED_DECIDER_BORDER
from queuemo.recipes import decider_border
from queuemo.recipes import feedback_decider_border
from queuemo.recipes import publish


def require():
    return 'rawmaker'


def run(rawspace: str):
    decider_border(rawspace, 'rawmaker')
    feedback_decider_border(rawspace, 'decider_border')


def after(rawspace: str):
    # TODO: replace with public vars of feedback_decider_border!
    decider_out = FEED_DECIDER_BORDER + '/feedback_decider_border__hitthebox_result.html'
    publish(rawspace, decider_out, 'layout/pages/border')
