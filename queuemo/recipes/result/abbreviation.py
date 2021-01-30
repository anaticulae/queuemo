# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation
============
"""

import iamraw.sections

import queuemo.runnable
import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    pages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.AbbreviationTable,
    )
    queuemo.runnable.groupme(
        inpath=[
            flow.tmppath,
            flow.general,
        ],
        output=flow.tmppath,
        abbreviation=True,
        pages=pages,
    )
    queuemo.runnable.decider_abbreviation(
        inpath=[
            flow.tmppath,
        ],
        output=flow.tmppath,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()
