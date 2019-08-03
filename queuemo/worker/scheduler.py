# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Watchdog for todo folder to listen to incoming jobs"""

from os import listdir
from os import makedirs
from os.path import exists
from os.path import join
from shutil import copytree
from shutil import rmtree
from time import sleep

from configo import ready
from configo import todo
from link import JOB_FILE_NAME
from link import job_dump
from link import job_load
from link import ready_count
from utila import FAILURE
from utila import SUCCESS
from utila import error
from utila import file_create
from utila import file_read
from utila import file_remove
from utila import log
from utila import log_stacktrace
from utila import tmpfile

from queuemo import ROOT
from queuemo.recipe import run as run_recipe

MAX_RUNTIME = 60 * 60 * 24 * 365  # Run one year
WAITING = 1000  # ms, 1 second


def run(runtime=MAX_RUNTIME, waiting=WAITING, verbose: bool = True):
    """Run the scheduler

    Args:
        runtime():
        waiting():
    Returns:
        SUCCESS when scheduler ends, or Exception, when runtime error occurs
    """
    if not waiting:
        waiting = 1
    tick = 0
    while tick < runtime:
        job = nextjob()
        try:
            step(job, waiting=waiting, verbose=verbose)
        except Exception:  # pylint: disable=broad-except
            log_stacktrace()
            error('\nClose scheduler: %d' % tick)
            return FAILURE
        tick += 1
        if not verbose and tick % 80 == 0:
            log()  # write newline

    log('\nTerminated: %d' % tick)
    return SUCCESS


def step(job, waiting=WAITING, verbose: bool = True):

    if not job:
        if verbose:
            log('Wait...')
        else:
            log('.', end='')
        sleep(waiting / 1000)  # miliseconds to seconds
    else:
        if not verbose:
            log()  # write newline
        log('Run job')
        if verbose:
            log('  Copy job')
        workspace = copy(job)

        if verbose:
            log('  Start job')
        work(workspace)

        push_result(workspace)
        if verbose:
            log('Finished')


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
        # already in progress
        if exists(check_ready):
            continue
        # Mark folder as in progress and start with 0 percent
        file_create(check_ready, '000')
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

    workspace = tmpfile(ROOT)

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

    log('Push result to: %s' % ready_path)
    # Copy results
    copytree(result, join(ready_path, 'result'))
    # Copy info.yaml
    info = file_read(join(workspace, JOB_FILE_NAME))
    file_create(join(ready_path, JOB_FILE_NAME), info)

    ready_after = ready_count()

    assert ready_before + 1 == ready_after

    assert todo(), todo()
    assert index, index
    current_todo = join(todo(), index)
    assert exists(current_todo)
    log('Remove todo: %s' % current_todo)
    rmtree(current_todo)
    # Wait till deletion is completed
    # TODO: Investigate here! Increase sleep? Check if todo is already in ready
    sleep(1)
    log('Remove temp: %s' % workspace)


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
    info.result = '%d' % result

    file_remove(info_path)  # remove old one to replace with new one
    job_dump(info_path, info)


def jobid(path: str):
    info_path = join(path, JOB_FILE_NAME)
    assert exists(info_path)
    info = job_load(info_path)
    return info.index
