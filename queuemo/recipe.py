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

import functools
import os
import shutil

import utila
import utila.test

import queuemo
import queuemo.api
import queuemo.recipes.analysis
import queuemo.recipes.commonview
import queuemo.recipes.docsplit
import queuemo.recipes.extractraw
import queuemo.recipes.resultview
import queuemo.recipes.runner
import queuemo.recipes.setup
import queuemo.recipes.validation

RUNNER = [
    'analysis_statistica',
    'decider_border',
    'feedback_decider_border',
    'feedback_statistica',
    'groupme',
    'rawmaker',
]
RECIPES = os.path.join(queuemo.ROOT, 'queuemo', 'recipes')

FASTVIEW = queuemo.recipes.scheduler.load(os.path.join(RECIPES, 'fastview'))


def run(workspace: str, document: str, outpath: str) -> int:
    check(workspace)

    runtime = queuemo.recipes.runner.RecipeRuntime(
        workspace=workspace,
        document=document,
        outpath=outpath,
    )
    runtime.append(FASTVIEW)

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


def run_step(workspace: str, step: str, inpath: str, outpath: str = None):
    # if outpath is not defined use step-name as outpath
    outpath = outpath if outpath != '' else step
    log_process_start(step)
    assert os.path.exists(workspace), workspace
    process = functools.partial(utila.test.run, cwd=workspace)
    inpath = os.path.join(workspace, inpath)
    outpath = os.path.join(workspace, outpath)
    completed = process('%s -i %s -o %s' % (
        step,
        inpath,
        outpath,
    ))
    utila.log(completed.stdout)
    assert completed.returncode == utila.SUCCESS, completed.stdout + completed.stderr
    assert os.path.exists(outpath)


# def run_raw(workspace, document: int):
#     # TODO: Automate add parallize order of recipes
#     utila.log('run recipe')

#     queuemo.recipes.validation.run(workspace, document)

#     queuemo.recipes.fastview_old.run(workspace, document)

#     queuemo.recipes.resultview.run(workspace, document)

#     utila.log('end recipe')
#     return


def run_recipe(workspace: str, todo):
    raw = os.path.join(workspace, 'raw')
    for step in todo:
        if isinstance(step, queuemo.api.Step):
            run_step(raw, step.process, step.inpath, step.outpath)
            continue
        if isinstance(step, queuemo.api.RawCopy):
            step.source = 'raw/' + step.source
            step.destination = 'raw/' + step.destination
        elif isinstance(step, queuemo.api.Publish):
            step.source = 'raw/' + step.source
            step.destination = 'result/' + step.destination

        source = os.path.join(workspace, step.source)
        dest = os.path.join(workspace, step.destination)
        if os.path.isfile(source):
            # Create base path
            os.makedirs(os.path.split(dest)[0], exist_ok=True)
            shutil.copy(source, dest)
        else:
            copy_content(source, dest)


def log_process_start(process):
    utila.log(' run %s' % process)


def copy_content(source, destination):
    """Copy the content from `source` to `destination` folder. If `desitination`
    folder does not exists, it will created."""
    assert os.path.exists(source), source
    os.makedirs(destination, exist_ok=True)
    # TODO: USE UTILA CODE?
    for item in os.listdir(source):
        shutil.copy(os.path.join(source, item), os.path.join(destination, item))
