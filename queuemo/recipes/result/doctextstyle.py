# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


# TODO: DUPLICATED IN TEXTFLOW, ADD AUTOMATIC SCHEDULER LATER
def before(flow: queuemo.runtime.api.RecipeIO):  # pylint:disable=W0613
    # RUN MAGIC BEFORE
    # TODO: ADD TEST THAT MAGIC EXISTS?
    pages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    queuemo.runnable.textflow_wordspace(
        inpath=[flow.general],
        output=flow.tmppath,
        pages=pages,
    )


def run(flow: queuemo.runtime.api.RecipeIO):
    content = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.MainPart,
    )
    queuemo.runnable.doctextstyle(
        inpath=[flow.general],
        output=flow.tmppath,
        pages=content,
    )
    queuemo.runnable.decider_textstyle_headlines(
        inpath=[flow.tmppath, flow.general],
        output=flow.tmppath,
        pages=content,
    )
    queuemo.runnable.decider_textstyle_text(
        inpath=[
            flow.package('magic'),  # required to skip tables etc.
            flow.tmppath,
            flow.general,
        ],
        output=flow.tmppath,
        pages=content,
    )


def after(flow: queuemo.runtime.api.RecipeIO):
    flow.publish_linting()

    resultview = link.resultview(flow.document)
    # TODO: REMOVE LATER
    if not os.path.exists(resultview):
        return
    # copy detected required style information to display in user
    # interface.
    utila.copy_content(
        flow.tmppath,
        resultview,
        pattern='doctextstyle__textstyle.yaml',
        verbose=True,
    )
    utila.copy_content(
        flow.general,
        resultview,
        pattern='rawmaker_*fonts_*.yaml',
        verbose=True,
    )
