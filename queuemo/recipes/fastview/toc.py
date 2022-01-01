# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections

import queuemo.runnable
import queuemo.runtime.api
import queuemo.utils

PREFIX = '05'


def run(flow: queuemo.runtime.api.RecipeIO):
    if flow.skip(queuemo.runnable.decider_toc):
        return
    tocpage = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.TableOfContent,
    )
    queuemo.runnable.groupme(
        flow.general,
        flow.tmppath,
        toc=True,
        pages=tocpage,
    )
    queuemo.runnable.decider_toc(
        inpath=[
            flow.general,
            flow.tmppath,
        ],
        outpath=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()
