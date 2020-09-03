# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections
import link
import utila

import queuemo.recipes
import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils


def before(flow: queuemo.runtime.api.RecipeIO):
    pages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    queuemo.runnable.words(
        inpath=[flow.general],
        output=flow.general,
        pages=pages,
    )
    queuemo.runnable.doctextstyle(
        inpath=flow.general,
        output=flow.general,
        pages=pages,
    )
    queuemo.runnable.caption(
        inpath=flow.general,
        output=flow.general,
        pages=pages,
    )
    queuemo.runnable.detector_formula(
        inpath=flow.general,
        outpath=flow.general,
        pages=pages,
    )
    queuemo.runnable.magic(
        inpath=flow.general,
        output=flow.general,
        pages=pages,
    )


def run(flow: queuemo.runtime.api.RecipeIO):
    pages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    queuemo.runnable.textflow_lineending(
        inpath=[flow.general],
        output=flow.tmppath,
        # pages=pages,
    )
    queuemo.runnable.decider_textflow_lineending(
        inpath=[
            flow.tmppath,
            flow.general,
        ],
        output=flow.tmppath,
        pages=pages,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

    resultview = link.resultview(flow.document)

    # TODO: REMOVE LATER?
    utila.copy_content(
        flow.general,
        resultview,
        pattern='words__word_result.yaml',
        verbose=True,
    )

    utila.copy_content(
        flow.general,
        resultview,
        pattern='caption__general_general.yaml',
        verbose=True,
    )
