# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json
import os

import link
import serializeraw
import utila

import queuemo
import queuemo.runnable
import queuemo.runtime.api
import queuemo.runtime.runtime


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    todo = link.todo(flow.document)
    assert os.path.exists(todo), f'todo does not exists: {todo}'
    link.start_progress(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO) -> list:
    """Run validation to check that """
    link.verify(flow.document)
    # TODO: add pdfinfo --status to check if validation was successful
    pdfinfo = link.pdfinfo(flow.document)
    loaded = utila.file_read(pdfinfo)
    validated = json.loads(loaded)
    if validated:
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
    content = any([
        len(page) for page in serializeraw.create_pagetextnavigators_frompath(
            flow.tmppath)
    ])
    if content:
        return
    utila.error(f'no text in resource {flow.sourcepath}, stop analysis.')
    raise queuemo.runtime.runtime.Stop('no text content')
