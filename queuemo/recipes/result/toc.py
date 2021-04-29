# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Toc
===
"""

import iamraw.sections
import utila

import queuemo.runnable
import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    pages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.TableOfContent,
    )
    if pages == ':':
        utila.info('could not detect TableOfContent page-numbers')
        return
    queuemo.runnable.groupme(
        inpath=[flow.general],
        output=flow.general,
        toc=True,
        pages=pages,
    )
