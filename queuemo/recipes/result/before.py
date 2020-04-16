# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila

import queuemo.runnable
import queuemo.runtime.api
import queuemo.runtime.runtime


def before(flow: queuemo.runtime.api.RecipeIO):
    if link.current(flow.document) == link.ProcessState.VERIFIED:
        # if fastview is not started before, start analysis with resultview
        link.start_analysis(flow.document)


def run(flow: queuemo.runtime.api.RecipeIO):
    pdf = flow.sourcepath

    completed = queuemo.runnable.rawmaker(
        inpath=pdf,
        outpath=flow.tmppath,
    )
    assert completed == utila.SUCCESS, str(completed)

    completed = queuemo.runnable.rawmaker(
        inpath=pdf,
        outpath=flow.tmppath,
        prefix='oneline',
        boxes_flow=1.0,
        char_margin=100,
        line_margin=0.1,
    )
    assert completed == utila.SUCCESS, str(completed)

    completed = queuemo.runnable.linero(
        inpath=flow.tmppath,
        output=flow.tmppath,
    )
    assert completed == utila.SUCCESS, str(completed)
    return [completed]
