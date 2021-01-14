# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import link
import utila

import queuemo
import queuemo.runnable
import queuemo.runtime.api


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    if link.current(flow.document) == link.ProcessState.VERIFIED:
        # if fastview is not started before, start analysis with resultview
        link.start_analysis(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    unpack_pdf(flow)

    determine_sections(flow)

    # ensure rawmaker is completed before running linero
    completed = queuemo.runnable.linero(
        inpath=flow.tmppath,
        output=flow.tmppath,
    )
    queuemo.runnable.groupme(
        inpath=[flow.tmppath],
        output=flow.tmppath,
    )
    assert completed == utila.SUCCESS, str(completed)
    return [completed]


def unpack_pdf(flow: queuemo.runtime.api.RecipeIO):
    pdf = flow.sourcepath
    with utila.GeorgFork() as fork:  # pylint:disable=E1101
        fork.append(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            all=True,
        )
        fork.append(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            prefix='oneline',
            boxes_flow=1.0,
            char_margin=100,
            line_margin=0.1,
            text=True,
            fonts=True,
        )
        fork.append(
            queuemo.runnable.spacestation,
            inpath=pdf,
            output=flow.tmppath,
        )
    assert fork.result == utila.SUCCESS, 'could not extract pdf'


def determine_sections(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.groupme(
        inpath=[flow.tmppath],
        output=flow.tmppath,
        pagenumbers=True,
        footer=True,
    )

    # determine to run area of feature detection
    queuemo.runnable.sections(
        inpath=flow.tmppath,
        output=flow.tmppath,
    )
