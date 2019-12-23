# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
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

from functools import partial
from os import listdir
from os import makedirs
from os.path import exists
from os.path import isfile
from os.path import join
from os.path import split
from shutil import copy

from utila import SUCCESS
from utila import call
from utila import error
from utila import log
from utila.test import run as _run_target

import queuemo.recipes.analysis as analysis
import queuemo.recipes.commonview as commonview
import queuemo.recipes.decider.border as decider_border
import queuemo.recipes.decider.fonts as decider_fonts
import queuemo.recipes.docsplit as docsplit
import queuemo.recipes.extractraw as extractraw
import queuemo.recipes.setup as setup
from queuemo import ROOT
from queuemo.api import Publish
from queuemo.api import RawCopy
from queuemo.api import Step

RUNNER = [
    'analysis_statistica',
    'decider_border',
    'feedback_decider_border',
    # 'feedback_statistica',
    'groupme',
    'rawmaker',
]


def run(workspace, document: int) -> int:
    check(workspace)
    run_raw(workspace, document)

    # TODO: We need a custom result
    return 95


def check(workspace: str):
    ret = 0
    for item in RUNNER:
        log(' check %s ' % item, end='')
        result = _run_target('%s --version' % item, workspace)
        log(result.stdout.strip())
        if result.returncode:
            error('Could not run %s' % item)
            error(str(result))
        ret += result.returncode
    if ret:
        exit(ret)
    log()  # add newline


def run_step(workspace: str, step: str, inpath: str, outpath: str = None):
    # if outpath is not definied use step-name as outpath
    outpath = outpath if outpath != '' else step
    log_process_start(step)
    assert exists(workspace), workspace
    process = partial(_run_target, cwd=workspace)
    inpath = join(workspace, inpath)
    outpath = join(workspace, outpath)
    completed = process('%s -i %s -o %s' % (
        step,
        inpath,
        outpath,
    ))
    log(completed.stdout)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr
    assert exists(outpath)


def run_raw(workspace, document: int):
    # TODO: Automate add parallize order of recipes
    log('run recipe')

    rawspace = join(workspace, 'raw')

    call('setup: before')
    setup.before(workspace)
    call('setup: run')
    setup.run(workspace, document)

    extractraw.run(rawspace)

    analysis.before(rawspace)
    analysis.run(rawspace)
    analysis.after(rawspace)

    decider_border.run(rawspace)
    decider_border.after(rawspace)

    decider_fonts.before(rawspace)
    decider_fonts.run(rawspace)
    decider_fonts.after(rawspace)

    docsplit.before(rawspace)
    docsplit.run(rawspace)

    commonview.before(rawspace)
    commonview.run(rawspace)
    commonview.after(rawspace)

    log('end recipe')
    return


def run_recipe(workspace: str, todo):
    raw = join(workspace, 'raw')
    for step in todo:
        if isinstance(step, Step):
            run_step(raw, step.process, step.inpath, step.outpath)
            continue
        if isinstance(step, RawCopy):
            step.source = 'raw/' + step.source
            step.destination = 'raw/' + step.destination
        elif isinstance(step, Publish):
            step.source = 'raw/' + step.source
            step.destination = 'result/' + step.destination

        source = join(workspace, step.source)
        dest = join(workspace, step.destination)
        if isfile(source):
            # Create base path
            makedirs(split(dest)[0], exist_ok=True)
            copy(source, dest)
        else:
            copy_content(source, dest)


def log_process_start(process):
    log(' run %s' % process)


def copy_content(source, destination):
    """Copy the content from `source` to `destination` folder. If `desitination`
    folder does not exists, it will created."""
    assert exists(source), source
    makedirs(destination, exist_ok=True)
    for item in listdir(source):
        copy(join(source, item), join(destination, item))
