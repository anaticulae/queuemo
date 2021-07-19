# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import link
import utila

import queuemo
import queuemo.recipes.utils
import queuemo.runnable
import queuemo.runtime.api

TIMEOUT_RESULT_TABLERO = configo.HV_INT_PLUS(default=120)


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    if link.current(flow.document) == link.ProcessState.VERIFIED:
        # if fastview is not started before, start analysis with resultview
        link.start_analysis(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    unpack_pdf(flow)

    queuemo.recipes.utils.determine_sections(flow)

    timeout = utila.Timeout(
        seconds=TIMEOUT_RESULT_TABLERO.value,
        gracefully=True,
    )
    queuemo.runnable.groupme(
        inpath=flow.tmppath,
        output=flow.tmppath,
        pagenumbers=True,
        footer=True,
        content=True,
    )
    # TODO: REPLACE WITH TABLERO --rawfile later
    utila.file_copy(flow.sourcepath, os.path.join(flow.tmppath, 'table'))
    # ensure rawmaker is completed before running tablero
    queuemo.runnable.tablero(
        inpath=flow.tmppath,
        output=flow.tmppath,
        timeout=timeout,
    )
    queuemo.runnable.groupme(
        inpath=[flow.tmppath],
        output=flow.tmppath,
        toc=False,
        footer=False,
        pagenumbers=False,
        abbreviation=False,
        content=False,
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
