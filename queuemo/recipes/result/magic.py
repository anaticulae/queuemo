# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections
import link
import utila

import queuemo.runnable
import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    # TODO: VERIFY MAGIC STEP
    content = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    with utila.GeorgFork(process=False) as runtime:
        runtime.fork(
            queuemo.runnable.caption,
            inpath=[flow.general],
            outpath=flow.general,
            pages=content,
        )
        runtime.fork(
            queuemo.runnable.detector_formula,
            inpath=[flow.general],
            outpath=flow.general,
            pages=content,
        )
    # required for detecting tables
    queuemo.runnable.magic(
        inpath=[flow.tmppath, flow.general],
        outpath=flow.general,
        pages=content,
    )
    queuemo.runnable.words(
        inpath=[flow.general],
        outpath=flow.general,
        pages=content,
    )
    queuemo.runnable.textflow_quotes(
        inpath=[flow.general],
        outpath=flow.general,
        pages=content,
    )
    # run magic with words data again
    queuemo.runnable.magic(
        inpath=[flow.tmppath, flow.general],
        outpath=flow.general,
        pages=content,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    resultview = link.resultview(flow.document)
    utila.copy_content(
        flow.general,
        resultview,
        pattern='caption__general_general.yaml',
        verbose=True,
    )
