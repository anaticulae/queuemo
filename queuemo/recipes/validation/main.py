# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import link
import serializeraw
import utila

import queuemo
import queuemo.recipes.logger
import queuemo.runnable
import queuemo.runtime.api
import queuemo.runtime.runtime


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    # set logging start mark
    queuemo.recipes.logger.start()

    todo = link.todo(flow.document)
    assert os.path.exists(todo), f'todo does not exists: {todo}'
    link.start_progress(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO) -> list:
    """Run validation to check that """
    link.verify(flow.document)
    # TODO: add pdfinfo --status to check if validation was successful????
    pdfinfo = link.pdfinfo(flow.document)
    utila.debug(pdfinfo)
    if pdfinfo:
        if pdfinfo != iamraw.InvalidPDF:
            return
    utila.error(f'invalid resource {flow.sourcepath}, stop analysis.')
    raise queuemo.runtime.runtime.Stop('invald pdf resource')


@queuemo.required
def after(flow: queuemo.runtime.api.RecipeIO):
    # check that document contains some text content
    todo = os.path.join(link.todo(flow.document), flow.document)
    queuemo.runnable.rawmaker(
        inpath=todo,
        outpath=flow.tmppath,
        text=True,
        pages='0:10',
    )
    ptns = serializeraw.create_pagetextnavigators_frompath(flow.tmppath)
    content = any(len(page) for page in ptns)
    if content:
        return
    utila.error(f'no text in resource {flow.sourcepath}, stop analysis.')
    raise queuemo.runtime.runtime.Stop('no text content')
