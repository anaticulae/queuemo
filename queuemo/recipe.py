# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
DataMining: PDF ->
    RawMaker        -> text.yaml ->
    GroupMe         -> chapter.yaml ->

Analysis/Reporting:

    Statistica      -> statistic.yaml ->

Decider:

    MathStyle       -> style.yaml                   WordStyle

Feedback:

    Feedback        -> feedback.yaml                Feedback

Presentation:

    HTML VIEW

"""

import os

import utila
import utila.test

import queuemo
import queuemo.recipes.runner

# TODO: CHECK ONLY REQUIRED RUNNER
RUNNER = [
    'analysis_statistica',
    'decider_border',
    'feedback_decider_border',
    'feedback_statistica',
    'groupme',
    'rawmaker',
    'pdfinfo',
]
RECIPES = os.path.join(queuemo.ROOT, 'queuemo', 'recipes')

VALIDATION = queuemo.recipes.scheduler.load(os.path.join(RECIPES, 'validation'))
FASTVIEW = queuemo.recipes.scheduler.load(os.path.join(RECIPES, 'fastview'))
RESULT = queuemo.recipes.scheduler.load(os.path.join(RECIPES, 'result'))
PUBLISH = queuemo.recipes.scheduler.load(os.path.join(RECIPES, 'publish'))


def run(workspace: str, document: str, outpath: str) -> int:
    check(workspace)

    runtime = queuemo.recipes.runner.RecipeRuntime(
        workspace=workspace,
        document=document,
        outpath=outpath,
    )
    runtime.append(VALIDATION)
    runtime.append(FASTVIEW)
    runtime.append(RESULT)
    runtime.append(PUBLISH)

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
