# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utila

import queuemo
import queuemo.recipes.result.before
import queuemo.runnable
import queuemo.runtime.api


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    link.start_analysis(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO) -> list:
    unpack_pdf(flow)

    queuemo.recipes.result.before.determine_sections(flow)

    completed = queuemo.runnable.linero(
        inpath=flow.tmppath,
        output=flow.tmppath,
    )
    assert completed == utila.SUCCESS, str(completed)
    return [completed]


def unpack_pdf(flow: queuemo.runtime.api.RecipeIO):
    pdf = flow.sourcepath
    with utila.GeorgFork() as runtime:
        runtime.fork(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            all=True,
            images=False,
            figures=False,
            pages='0:10',
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
            pages='0:5',
        )
    assert runtime.result == utila.SUCCESS, 'could not extract pdf'
