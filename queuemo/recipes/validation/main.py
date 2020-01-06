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

import utila

import queuemo.recipes.api
import queuemo.recipes.runner


def run(flow: queuemo.recipes.api.RecipeIO) -> list:
    """Run validation to check that """
    completed = utila.run(f'pdfinfo -i {flow.sourcepath} -o {flow.outpath}')
    utila.log(f'write validation result to: {flow.outpath}')

    if completed.returncode:
        utila.error(completed.stderr + completed.stdout)
    assert completed.returncode == 0


def after(flow: queuemo.recipes.api.RecipeIO):
    # TODO: add pdfinfo --status to check if validation was successful
    pdfinfo = os.path.join(flow.outpath, 'pdfinfo.json')
    loaded = utila.file_read(pdfinfo)
    validated = json.loads(loaded)
    if validated:
        return
    utila.log(f'invalid resource {flow.sourcepath}, stop analysis.')
    raise queuemo.recipes.runner.Stop('invald pdf resource')
