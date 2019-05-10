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

from dataclasses import dataclass
from functools import partial
from os import listdir
from os import makedirs
from os.path import exists
from os.path import isfile
from os.path import join
from os.path import split
from shutil import copy

from utila import SUCCESS
from utila import logging
from utila import logging_error
from utila.test import run as _run_target

RUNNER = [
    'analysis_statistica',
    'decider_border',
    'feedback_decider_border',
    'feedback_statistica',
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
        logging(' check %s ' % item, end='')
        result = _run_target('%s --version' % item, workspace)
        logging(result.stdout.strip())
        if result.returncode:
            logging_error('Could not run %s' % item)
            logging_error(str(result))
        ret += result.returncode
    if ret:
        exit(ret)
    logging()  # add newline


@dataclass
class Step:
    process: str
    inpath: str
    outpath: str = ''


@dataclass
class Copy:
    source: str
    destination: str


class RawCopy(Copy):
    pass


class Publish(Copy):
    pass


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
    logging(completed.stdout)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr
    assert exists(outpath)


def run_raw(workspace, document: int):
    logging('Run recipe')
    raw = join(workspace, 'raw')
    result = join(workspace, 'result')

    makedirs(raw)
    makedirs(result, exist_ok=True)

    pdf = join(workspace, document)
    assert exists(pdf)

    # extract pdf file
    copy(pdf, join(workspace, 'work.pdf'))
    # TODO: Use more public vars
    todo = [
        Step('rawmaker', '..'),
        Step('groupme', 'rawmaker'),
        Step('analysis_statistica', 'groupme'),
        RawCopy('groupme', 'feedback_statistica_input'),
        RawCopy('analysis_statistica', 'feedback_statistica_input'),
        Step('feedback_statistica', 'feedback_statistica_input'),
        # publish
        Publish('feedback_statistica/feedback_statistica__chapter.html',
                '06_statistica/05_chapter/05_sections/index.html'),
        Publish('feedback_statistica/feedback_statistica__words.html',
                '06_statistica/06_chapter/06_words/index.html'),
        # decider
        Step('decider_border', 'rawmaker'),
        Step('feedback_decider_border', 'decider_border'),
        # publish
        Publish('feedback_decider_border/hitthebox_view__result.html',
                '02_layout/04_pages/06_border/index.html'),
    ]

    run_recipe(workspace, todo)

    logging('End recipe')
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
    logging(' run %s' % process)


def copy_content(source, destination):
    """Copy the content from `source` to `destination` folder. If `desitination`
    folder does not exists, it will created."""
    assert exists(source), source
    makedirs(destination, exist_ok=True)
    for item in listdir(source):
        copy(join(source, item), join(destination, item))
