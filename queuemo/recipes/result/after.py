# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import protocol
import utila

import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    """Create a file named `done` to signal update handler that process
    is completed."""
    write_optimized_findings(flow.document)
    # TODO: ADD STATUS INFORMATION LATER
    link.finish_resultview(flow.document)


def write_optimized_findings(document: str):
    optimized = link.optimized(document, done=False)
    os.makedirs(optimized)
    utila.log((f'load: {link.resultview(document)} and '
               f'write optimized to: {optimized}'))
    findings = [
        pagefindings.content for pagefindings in protocol.findings_from_path(
            link.resultview(document))
    ]
    findings = utila.flatten(findings)
    findings = utila.not_none(findings)
    protocol.write_grouped(findings, optimized)
