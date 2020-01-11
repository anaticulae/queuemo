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

# TODO: CHECK ONLY REQUIRED RUNNER
RUNNER = [
    'analysis_statistica',
    'decider_border',
    'feedback_statistica',
    'groupme',
    'rawmaker',
    'pdfinfo',
]


def run(workspace: str, document: str, outpath: str) -> int:
    check(workspace)

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


def check(workspace: str):
    ret = 0
    for item in RUNNER:
        utila.log(' check %s ' % item, end='')
        result = utila.test.run('%s --version' % item, workspace)
        utila.log(result.stdout.strip())
        if result.returncode:
            utila.error('Could not run %s' % item)
            utila.error(str(result))
        ret += result.returncode
    if ret:
        exit(ret)
    utila.log()  # add newline
