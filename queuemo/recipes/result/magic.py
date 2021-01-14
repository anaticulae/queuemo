# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
    content = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    with utila.GeorgFork() as runtime:  # pylint:disable=E1101
        runtime.fork(
            queuemo.runnable.words,
            inpath=[flow.general],
            output=flow.general,
            pages=content,
        )
        runtime.fork(
            queuemo.runnable.caption,
            inpath=[flow.general],
            output=flow.general,
            pages=content,
        )
        runtime.fork(
            queuemo.runnable.detector_formula,
            inpath=[flow.general],
            outpath=flow.general,
            pages=content,
        )
    queuemo.runnable.textflow_quotes(
        inpath=[flow.general],
        output=flow.general,
        pages=content,
    )
    # required for detecting tables
    queuemo.runnable.magic(
        inpath=flow.general,
        output=flow.general,
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
