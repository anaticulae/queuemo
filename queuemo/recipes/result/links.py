# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utila

import queuemo.runnable
import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.words_links(
        inpath=[flow.general],
        output=flow.tmppath,
    )
    queuemo.runnable.decider_links(
        inpath=[flow.tmppath],
        output=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

    resultview = link.resultview(flow.document)
    utila.copy_content(
        flow.general,
        resultview,
        pattern='words__links_links.yaml',
        verbose=True,
    )
