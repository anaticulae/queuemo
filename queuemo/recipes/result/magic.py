# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections
import link
import utilo

import queuemo.runnable
import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    # TODO: VERIFY MAGIC STEP
    content = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    with utilo.GeorgFork(process=False) as runtime:
        runtime.fork(
            queuemo.runnable.caption,
            inpath=flow.general,
            outpath=flow.general,
            pages=content,
        )
        runtime.fork(
            queuemo.runnable.detector_formula,
            inpath=flow.general,
            outpath=flow.general,
            pages=content,
        )
    # required for detecting tables
    queuemo.runnable.magic(
        inpath=[
            flow.tmppath,
            flow.general,
        ],
        outpath=flow.general,
        pages=content,
    )
    queuemo.runnable.headlines(
        inpath=flow.general,
        outpath=flow.general,
        pages=content,
    )
    queuemo.runnable.lists(
        inpath=flow.general,
        outpath=flow.general,
        pages=content,
    )
    queuemo.runnable.words(
        inpath=flow.general,
        outpath=flow.general,
        pages=content,
    )
    queuemo.runnable.textflow_quotes(
        inpath=flow.general,
        outpath=flow.general,
        pages=content,
    )
    # run magic with words data again
    queuemo.runnable.magic(
        inpath=[
            flow.tmppath,
            flow.general,
        ],
        outpath=flow.general,
        pages=content,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    resultview = link.resultview(flow.document)
    caption_path = iamraw.path.caption_result(flow.general)
    if not utilo.exists(caption_path):
        return
    utilo.log(f'cp: {caption_path} -> {resultview}')
    utilo.file_copy(
        caption_path,
        resultview,
    )
