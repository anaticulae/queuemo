# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import qvlink

import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    """Create a file named `done` to signal update handler that process
    is completed."""
    # TODO: ADD STATUS INFORMATION LATER
    qvlink.finish_resultview(flow.document)
