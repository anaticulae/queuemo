# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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

from os import listdir
from os import makedirs
from os.path import exists
from os.path import join
from shutil import copy
from shutil import copytree

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

    return 95


def check(workspace: str):
    ret = 0
    for item in RUNNER:
        logging('check %s' % item)
        result = _run_target('%s --help' % item, workspace)
        if result.returncode:
            logging_error('Could not run %s' % item)
            logging_error(str(result))
        ret += result.returncode
    if ret:
        exit(ret)


def run_raw(workspace, document: int):
    raw_path = join(workspace, 'raw')
    makedirs(raw_path)
    pdf = join(workspace, document)
    assert exists(pdf)

    # extract pdf file
    copy(pdf, join(workspace, 'work.pdf'))

    rawmaker_output = join(raw_path, 'rawmaker')
    completed = _run_target(
        'rawmaker -i %s -o %s' % (workspace, rawmaker_output),
        workspace,
    )
    logging(completed.stdout)
    assert completed.returncode == SUCCESS, str(completed)
    assert exists(rawmaker_output)

    groupme_output = join(raw_path, 'groupme')
    completed = _run_target(
        'groupme -i %s -o %s' % (rawmaker_output, groupme_output),
        workspace,
    )
    assert completed.returncode == SUCCESS, str(completed)

    # analysis_statistica_input = join(raw_path, 'analysis_statistica_input')
    # Analysis statistica requires the output of two processes:
    #   rawmaker
    #   groupme
    # copy_content(rawmaker_output, analysis_statistica_input)
    # copy_content(groupme_output, analysis_statistica_input)

    statistica_output = join(raw_path, 'analysis_statistica')
    completed = _run_target(
        'analysis_statistica -i %s -o %s' % (groupme_output, statistica_output),
        workspace)
    assert completed.returncode == SUCCESS, str(completed)

    # result_index = join(raw_path, 'result.html')
    # completed = _run_target(
    #     'feedback_statistica -i %s -o %s' % (chapter_and_measure, result_index),
    #     workspace,
    # )
    # assert completed.returncode == SUCCESS, str(completed)


def copy_content(source, destination):
    """Copy the content from `source` to `destination` folder. If `desitination`
    folder does not exists, it will created."""
    assert exists(source)
    makedirs(destination, exist_ok=True)
    for item in listdir(source):
        copy(join(source, item), join(destination, item))
