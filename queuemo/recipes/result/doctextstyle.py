# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila

import queuemo.recipes
import queuemo.runnable
import queuemo.runtime.api


# TODO: DUPLICATED IN TEXTFLOW, ADD AUTOMATIC SCHEDULER LATER
def before(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.sections(
        inpath=[flow.general],
        output=flow.general,
    )
    queuemo.runnable.words(
        inpath=[flow.general],
        output=flow.general,
    )


def run(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.doctextstyle(
        inpath=[flow.general],
        output=flow.tmppath,
    )
    queuemo.runnable.decider_textstyle_headlines(
        inpath=[flow.tmppath, flow.general],
        output=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

    resultview = link.resultview(flow.document)
    # TODO: REMOVE LATER
    if not os.path.exists(resultview):
        return
    # copy detected required style information to display in user
    # interface.
    utila.copy_content(
        flow.tmppath,
        resultview,
        pattern='doctextstyle__textstyle.yaml',
        verbose=True,
    )
