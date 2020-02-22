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
    link.start_analysis(flow.document)


def run(flow: queuemo.runtime.api.RecipeIO) -> list:
    # TODO: REMOVE AFTER UPGRADING RAWMAKER WHICH SUPPORTS FILES AS INPUT
    pdf = os.path.join(flow.tmppath, 'work.pdf')
    utila.file_copy(flow.sourcepath, pdf)

    completed = queuemo.runnable.rawmaker(
        inpath=pdf,
        outpath=flow.tmppath,
        prefix='oneline',
        pages='0',
        # TODO: use rawmaker parameter! Refactor run interface
        boxes_flow=1.0,
        char_margin=100,
        line_margin=0.1,
    )
    assert completed == utila.SUCCESS, str(completed)

    # TODO: RUN IN PARALLEL
    # TODO: ADD TOC SELECTOR to find locatino of table of content
    completed = queuemo.runnable.rawmaker(
        inpath=pdf,
        outpath=flow.tmppath,
        pages='0:10',
    )
    assert completed == utila.SUCCESS, str(completed)

    completed = queuemo.runnable.linero(
        inpath=flow.tmppath,
        output=flow.tmppath,
    )
    assert completed == utila.SUCCESS, str(completed)

    return [completed]
