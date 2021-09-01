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
import layout
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
    # ensure that todo path exists
    todo = link.todo(flow.document)
    assert os.path.exists(todo), f'todo does not exists: {todo}'
    link.start_progress(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO) -> list:
    """Run validation to check that document is analyzable."""
    link.verify(flow.document)
    # TODO: add pdfinfo --status to check if validation was successful????
    pdfinfo = link.pdfinfo(flow.document)
    utila.debug(pdfinfo)
    if not pdfinfo:
        msg = f'could not locate {flow.document}:{pdfinfo}'
        utila.error(msg)
        raise queuemo.runtime.runtime.Stop(msg)
    if pdfinfo == iamraw.InvalidPDF:
        utila.error(f'invalid resource {flow.sourcepath}, stop analysis.')
        raise queuemo.runtime.runtime.Stop('invald pdf resource')
    if flow.config.skip_unsupported:
        # TODO: REPLACE WITH ABEL LATER
        document_layout = layout.document_layout(
            flow.sourcepath,
            pages=utila.ranged_tuple(0, 30),
        )
        if iamraw.Layout.DOUBLECOLUMN in document_layout:
            msg = f'double column not supported: {flow.sourcepath}'
            utila.error(msg)
            raise queuemo.runtime.runtime.NotSupported(msg)


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
