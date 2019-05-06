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
from os.path import join
from shutil import copy

from utila import SUCCESS
from utila import logging
from utila import logging_error
from utila.test import run as _run_target

RUNNER = [
    'feedback_statistica',
    'groupme',
    'rawmaker',
    'analysis_statistica',
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


def run_raw(workspace, document: int):
    logging('Run recipe')
    raw_path = join(workspace, 'raw')
    result_path = join(workspace, 'result')

    makedirs(raw_path)
    makedirs(result_path, exist_ok=True)

    pdf = join(workspace, document)
    assert exists(pdf)

    # extract pdf file
    copy(pdf, join(workspace, 'work.pdf'))

    log_process_start('rawmaker')
    process = partial(_run_target, cwd=workspace)
    rawmaker_output = join(raw_path, 'rawmaker')
    completed = process('%s -i %s -o %s' % (
        'rawmaker',
        workspace,
        rawmaker_output,
    ))
    logging(completed.stdout)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr
    assert exists(rawmaker_output)

    log_process_start('groupme')
    groupme_output = join(raw_path, 'groupme')
    completed = process('%s -i %s -o %s' % (
        'groupme',
        rawmaker_output,
        groupme_output,
    ))
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr

    log_process_start('analysis_statistica')
    statistica_output = join(raw_path, 'analysis_statistica')
    completed = process('%s -i %s -o %s' % (
        'analysis_statistica',
        groupme_output,
        statistica_output,
    ))
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr

    log_process_start('feedback_analysis_statistica')
    feedback_statistica_input = join(raw_path, 'feedback_statistica_input')
    # Analysis statistica feedback requires the output of two processes:
    #   rawmaker
    #   groupme
    copy_content(groupme_output, feedback_statistica_input)
    # copy_content(rawmaker_output, feedback_statistica_input)
    copy_content(statistica_output, feedback_statistica_input)

    feedback_statistica_output = join(raw_path, 'analysis_statistica')
    completed = process('%s -i %s -o %s' % (
        'feedback_statistica',
        feedback_statistica_input,
        feedback_statistica_output,
    ))
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr

    log_process_start('publish')
    goal_sections = join(result_path, '06_statistica/05_chapter/05_sections')
    goal_words = join(result_path, '06_statistica/05_chapter/05_words')
    makedirs(goal_sections)
    makedirs(goal_words)

    copy(
        join(feedback_statistica_output, 'feedback_statistica__chapter.html'),
        join(goal_sections, 'index.html'))
    copy(
        join(feedback_statistica_output, 'feedback_statistica__words.html'),
        join(goal_words, 'index.html'))

    logging('End recipe')


def log_process_start(process):
    logging(' run %s' % process)


def copy_content(source, destination):
    """Copy the content from `source` to `destination` folder. If `desitination`
    folder does not exists, it will created."""
    assert exists(source)
    makedirs(destination, exist_ok=True)
    for item in listdir(source):
        copy(join(source, item), join(destination, item))
