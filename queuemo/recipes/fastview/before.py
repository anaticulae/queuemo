# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import queuemo.recipes.api
import queuemo.recipes.runner


def run(flow: queuemo.recipes.api.RecipeIO) -> list:
    # TODO: REMOVE AFTER UPGRADING RAWMAKER WHICH SUPPORTS FILES AS INPUT
    pdf = os.path.join(flow.tmppath, 'work.pdf')
    utila.file_copy(flow.sourcepath, pdf)

    completed = queuemo.recipes.rawmaker(
        inpath=pdf,
        outpath=flow.tmppath,
        prefix='oneline',
        pages='0',
    )
    assert completed == utila.SUCCESS, str(completed)
    return [completed]
