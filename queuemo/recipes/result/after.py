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


def run(flow: queuemo.recipes.api.RecipeIO):
    """Create a file named close to signal update hander that process is
    completed."""
    # TODO: REPLACE WITH LINK CODE
    donepath = os.path.join(flow.outpath, 'done')
    # TODO: ADD STATUS INFORMATION LATER
    utila.file_create(donepath)
