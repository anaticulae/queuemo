# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Watchdog for todo folder to listen to incoming jobs"""

from os import listdir
from os import makedirs
from os.path import exists
from os.path import join
from shutil import copytree
from time import sleep

from configo import ready
from configo import todo
from link import JOB_FILE_NAME
from link import job_dump
from link import job_load
from link import ready_count
from utila import SUCCESS
from utila import file_create
from utila import file_read
from utila import file_remove
from utila import logging
from utila import tempfile

from queuemo import ROOT
from queuemo.receipe import run as run_receipe

WAIT_FOR_NEXT_JOB = 1  # in seconds

MAX_RUNTIME = 60 * 60 * 24 * 365  # Run one year


def run():
    tick = 0
    while tick < MAX_RUNTIME:
        job = nextjob()
        step(job)
        tick += 1
    logging('Terminated: %d' % tick)

    return SUCCESS


def step(job):
    if not job:
        logging('Wait...')
        sleep(WAIT_FOR_NEXT_JOB)
    else:
        logging('Copy job')
        workspace = copy(job)

        logging('Start job')
        work(workspace)

        push_result(workspace)
        logging('Finished')


def nextjob():
    """Find next job and mark it as `in progress`

    Select the todo folder and search for a folder that does not include an
    `inprogress` file.

    Returns:
        If there is a matching file, return the folder name as jobid
        If there is no matching file than return `None`
    """

    todopath = todo(True)
    for item in listdir(todopath):
        check_ready = join(todopath, item, 'inprogress')
        if not exists(check_ready):
            continue
        # Mark folder as in progress
        file_create(check_ready)
        makedirs(check_ready)
        return item
    return None


def copy(job):
    """Copy job to temporary workspace folder

    Args:
        job(int):
    Returns:
        path to temporary workspace
    """
    path = join(todo(), job)
    assert exists(path), path

    workspace = tempfile(ROOT)

    # copy todo folder
    copytree(path, workspace)

    return workspace


def push_result(workspace):
    assert exists(workspace)
    result = join(workspace, 'result')
    assert exists(result)

    ready_before = ready_count()

    index = jobid(workspace)
    ready_path = join(ready(), index)

    # Copy results
    copytree(result, ready_path)
    # Copy info.yaml
    info = file_read(join(workspace, JOB_FILE_NAME))
    file_create(join(ready_path, JOB_FILE_NAME), info)

    ready_after = ready_count()

    assert ready_before + 1 == ready_after


def work(workspace):
    assert exists(workspace)
    result = join(workspace, 'result')
    makedirs(result)

    result = run_recipe(workspace, jobid(workspace))

    update_info(workspace, result)


def update_info(workspace, result: int):
    info_path = join(workspace, JOB_FILE_NAME)
    assert exists(info_path)
    info = job_load(info_path)
    info.result = '%d percent' % result

    file_remove(info_path)  # remove old one to replace with new one
    job_dump(info_path, info)


def jobid(path: str):
    info_path = join(path, JOB_FILE_NAME)
    assert exists(info_path)
    info = job_load(info_path)
    return info.index
