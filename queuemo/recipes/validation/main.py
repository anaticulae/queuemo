# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import json

import link
import utila

import queuemo.runtime.api
import queuemo.runtime.runtime


def before(flow: queuemo.runtime.api.RecipeIO):
    link.start_progress(flow.document)


def run(flow: queuemo.runtime.api.RecipeIO) -> list:
    """Run validation to check that """
    link.verify(flow.document)


def after(flow: queuemo.runtime.api.RecipeIO):
    # TODO: add pdfinfo --status to check if validation was successful
    pdfinfo = link.pdfinfo(flow.document)
    loaded = utila.file_read(pdfinfo)
    validated = json.loads(loaded)
    if validated:
        return
    utila.log(f'invalid resource {flow.sourcepath}, stop analysis.')
    raise queuemo.runtime.runtime.Stop('invald pdf resource')
