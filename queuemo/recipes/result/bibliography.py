# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Bibliography
============

1a. Extract area of bibliography
1b. Extract bibliography in detected area

2. Extract references to bibliography in the whole document

3a. Judge area of bibliography
3b. Judge reference to area of bibliography
"""

import os

import iamraw.sections
import qvlink
import utilo

import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils


def run(flow: queuemo.runtime.api.RecipeIO):
    if flow.skip(queuemo.runnable.decider_bibliography):
        return
    bibliography = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.Bibliography,
    )
    bibliography_references = queuemo.utils.select_pages(
        flow.general,
        select=(
            iamraw.sections.MainPart,
            iamraw.sections.Appendix,
        ),
        noselect=(iamraw.sections.Bibliography,),
    )
    with utilo.GeorgFork(process=False) as runtime:
        runtime.fork(
            queuemo.runnable.bibliography,
            inpath=flow.general,
            outpath=flow.tmppath,
            pages=bibliography,
        )
        runtime.fork(
            queuemo.runnable.docref_bibliography,
            inpath=flow.general,
            outpath=flow.tmppath,
            pages=bibliography_references,
        )
    queuemo.runnable.decider_bibliography(
        inpath=[
            flow.todopath,
            flow.package('intro'),  # REMOVE AFTER CHANGING DECIDER_BIB
            flow.tmppath,
            flow.general,
        ],
        outpath=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()
    resultview = qvlink.resultview(flow.document)
    # TODO: REMOVE LATER
    if not os.path.exists(resultview):
        return
    utilo.copy_content(
        flow.tmppath,
        resultview,
        pattern='detector__bibliography_detected.yaml',
        verbose=True,
    )
    utilo.copy_content(
        flow.tmppath,
        os.path.join(resultview, 'view'),
        pattern='decider_bibliography__plot_year_histogram.png',
        verbose=True,
    )
