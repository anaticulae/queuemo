# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw.sections
import link
import utila

import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils


def run(flow: queuemo.runtime.api.RecipeIO):
    bibliography = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.Bibliography,
    )

    queuemo.runnable.bibliography(
        inpath=[flow.general],
        output=flow.tmppath,
        pages=bibliography,
    )
    queuemo.runnable.decider_bibliography(
        inpath=[
            flow.tmppath,
            flow.general,
        ],
        output=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

    resultview = link.resultview(flow.document)
    # TODO: REMOVE LATER
    if not os.path.exists(resultview):
        return
    utila.copy_content(
        flow.tmppath,
        resultview,
        pattern='detector__bibliography_detected.yaml',
        verbose=True,
    )
