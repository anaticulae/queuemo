# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import queuemo.runnable
import queuemo.runtime.api

PREFIX = '05'


def run(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.groupme(flow.general, flow.tmppath)
    queuemo.runnable.decider_toc(
        inpath=[
            flow.general,
            flow.tmppath,
        ],
        output=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()
