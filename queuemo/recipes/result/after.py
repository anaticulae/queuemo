# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link

import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    """Create a file named `done` to signal update handler that process
    is completed."""
    active = None
    if flow.config and flow.config.webconfig:
        # do not publish all findings, publish just select onces
        active = flow.config.webconfig.active
    link.write_optimized_findings(
        document=flow.document,
        active=active,
    )
    # TODO: ADD STATUS INFORMATION LATER
    link.finish_resultview(flow.document)
