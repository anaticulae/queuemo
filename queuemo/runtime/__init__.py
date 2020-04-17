# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Recipes Runtime
===============


"""

import utila
import utila.test

import queuemo
import queuemo.recipes
import queuemo.runnable

# TODO: CHECK ONLY REQUIRED RUNNER
# DUPLICATED: SEE OTHER RUNNER!
RUNNER = [
    # 'analysis_statistica',
    'decider_border',
    # 'feedback_statistica',
    'groupme',
    'rawmaker',
    'pdfinfo',
]


def run(workspace: str, document: str, outpath: str) -> int:
    queuemo.runnable.check(RUNNER)

    runtime = queuemo.runtime.runtime.RecipeRuntime(
        workspace=workspace,
        document=document,
        outpath=outpath,
    )

    for item in queuemo.recipes.ORDER:
        runtime.append(item)

    while True:
        current = runtime.next_step()
        if current is None:
            # Done, everthing completed successful.
            break
        if not current:
            # Failure
            break

    # TODO: We need a custom result
    return 95
