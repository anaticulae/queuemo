# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections

import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils


def run(flow: queuemo.runtime.api.RecipeIO):
    if flow.skip(queuemo.runnable.decider_chapter):
        return
    pages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    queuemo.runnable.chapter(
        inpath=flow.general,
        outpath=flow.tmppath,
        pages=pages,
    )
    queuemo.runnable.decider_chapter(
        inpath=[
            flow.tmppath,
            flow.general,
        ],
        outpath=flow.tmppath,
        pages=pages,
        **flow.docinfo_ifgiven,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()
