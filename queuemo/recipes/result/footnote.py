# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utila

import queuemo.runnable
import queuemo.runtime.api


def before(flow: queuemo.runtime.api.RecipeIO):  # pylint:disable=W0613
    # TODO: CHECK THAT WORDS IS RUNNED BEFORE
    pass


def run(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.decider_footnote(
        inpath=[flow.general],
        output=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

    resultview = link.resultview(flow.document)

    # TODO: REMOVE LATER?
    utila.copy_content(
        flow.general,
        resultview,
        pattern='groupme__footer_footerheader.yaml',
        verbose=True,
    )
