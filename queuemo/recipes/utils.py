# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import queuemo.runnable
import queuemo.runtime.api


def determine_sections(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.groupme(
        inpath=[flow.tmppath],
        output=flow.tmppath,
        pagenumbers=True,
        footer=True,
    )

    # determine to run area of feature detection
    queuemo.runnable.sections(
        inpath=flow.tmppath,
        output=flow.tmppath,
    )
