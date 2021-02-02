# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import link
import utila

import queuemo
import queuemo.runnable
import queuemo.runtime.api

TIMEOUT_RESULT_LINERO = configo.HV_INT_PLUS(default=120)


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    if link.current(flow.document) == link.ProcessState.VERIFIED:
        # if fastview is not started before, start analysis with resultview
        link.start_analysis(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    unpack_pdf(flow)

    determine_sections(flow)

    timeout = utila.Timeout(
        seconds=TIMEOUT_RESULT_LINERO.value,
        gracefully=True,
    )
    # ensure rawmaker is completed before running linero
    queuemo.runnable.linero(
        inpath=flow.tmppath,
        output=flow.tmppath,
        timeout=timeout,
    )
    queuemo.runnable.groupme(
        inpath=[flow.tmppath],
        output=flow.tmppath,
        footer=False,
        pagenumbers=False,
        abbreviation=False,
    )


def unpack_pdf(flow: queuemo.runtime.api.RecipeIO):
    pdf = flow.sourcepath
    with utila.GeorgFork(worker=2) as runtime:
        # use 2 worker to start spacestation after finishing first rawmaker
        runtime.fork(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            all=True,
        )
        runtime.fork(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            prefix='oneline',
            boxes_flow=1.0,
            char_margin=100,
            line_margin=0.1,
            text=True,
            fonts=True,
            process=1,
        )
        runtime.fork(
            queuemo.runnable.spacestation,
            inpath=pdf,
            output=flow.tmppath,
        )
    assert runtime.result == utila.SUCCESS, 'could not extract pdf'


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
