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
import queuemo.recipes.utils
import queuemo.runnable
import queuemo.runtime.api

TIMEOUT_FASTVIEW_TABLERO = configo.HV_INT_PLUS(default=60)
FIRST_PAGES = configo.HV_STR(default='0:10')


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    link.start_analysis(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO) -> list:
    unpack_pdf(flow)

    queuemo.recipes.utils.determine_sections(flow)

    # TODO: DO WE REQUIRE TABLES FOR FIRST 10 PAGES?
    # queuemo.runnable.groupme(
    #     inpath=flow.tmppath,
    #     outpath=flow.tmppath,
    #     pagenumbers=True,
    #     footer=True,
    #     content=True,
    # )
    # queuemo.runnable.tablero(
    #     inpath=flow.tmppath,
    #     outpath=flow.tmppath,
    #     table=flow.sourcepath,
    #     timeout=TIMEOUT_FASTVIEW_TABLERO.value,
    #     pages=FIRST_PAGES.value,
    # )


def unpack_pdf(flow: queuemo.runtime.api.RecipeIO):
    pdf = flow.sourcepath
    with utila.GeorgFork(process=False) as runtime:
        runtime.fork(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            all=True,
            images=False,
            figures=False,
            pages=FIRST_PAGES.value,
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
