# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Watchdog for todo folder to listen to incoming jobs"""
import os
import shutil
import time

import configo
import link
import utila

import queuemo
import queuemo.recipes
import queuemo.runtime
import queuemo.worker.progress

MAX_RUNTIME = 60 * 60 * 24 * 365  # Run one year
WAITING = 1000  # ms, 1 second


def run(
        runtime: float = MAX_RUNTIME,
        waiting: float = WAITING,
        verbose: bool = True,
) -> int:
    """Run the scheduler

    Args:
        runtime(float): runtime in seconds
        waiting(float): waiting time in mili-seconds
        verbose(bool): increase logging if True
    Returns:
        SUCCESS when scheduler ends, or Exception, when runtime error occurs
    """
    todopath = configo.todo(True)
    utila.log('start working on: %s' % todopath)
    utila.print_env()
    if not waiting:
        waiting = 1
    tick = 0
    while tick < runtime:
        job = nextjob()
        try:
            step(job, waiting=waiting, verbose=verbose)
        except Exception:  # pylint: disable=broad-except
            utila.log_stacktrace()
            utila.error('\nClose scheduler: %d' % tick)
            return utila.FAILURE
        tick += 1
        if not verbose and tick % 80 == 0:
            utila.log()  # write newline

    utila.log('\nTerminated: %d' % tick)
    return utila.SUCCESS


def step(job, waiting=WAITING, verbose: bool = True):
    if not job:
        if verbose:
            utila.log('Wait...')
        else:
            utila.log('.', end='')
        time.sleep(waiting / 1000)  # miliseconds to seconds
    else:
        if not verbose:
            utila.log()  # write newline
        utila.log('Run job')
        if verbose:
            utila.log('  Copy job')
        workspace = copy(job)

        if verbose:
            utila.log('  Start job')
        work(workspace)

        if verbose:
            utila.log('Finished')


def nextjob() -> int:
    """Find next job and mark it as `in progress`

    Select the todo folder and search for a folder that does not include
    an `inprogress` file. After finding an waiting job, starting them
    and return the `jobid` as nextjob.

    Returns:
        If there is a matching file, return the folder name as jobid
        If there is no matching file, return `None`
    """
    todopath = configo.todo(True)
    for jobnumber in os.listdir(todopath):
        itempath = os.path.join(todopath, jobnumber)
        if os.path.isfile(itempath):
            # require input folder, not a single file
            utila.error(f'file: not a input resource: {itempath}')
            continue
        if queuemo.worker.progress.inprogress(jobnumber):
            continue
        # return next job, start it by recipe runner
        return jobnumber
    return None


def copy(job):
    """Copy job to temporary workspace folder

    Args:
        job(int):
    Returns:
        path to temporary workspace
    """
    path = os.path.join(configo.todo(), job)
    assert os.path.exists(path), str(path)

    workspace = utila.tmpfile(queuemo.ROOT)

    # copy todo to temporary folder
    shutil.copytree(path, workspace)

    return workspace


def work(workspace):
    assert os.path.exists(workspace), str(workspace)
    current = jobid(workspace)
    outpath = os.path.join(configo.todo(), current)

    result = queuemo.runtime.run(workspace, jobid(workspace), outpath=outpath)

    update_info(outpath, result)


def update_info(workspace, result: int):
    info_path = os.path.join(workspace, link.JOB_FILE_NAME)
    assert os.path.exists(info_path), str(info_path)
    info = link.load_job(info_path)
    info.result = '%d' % result

    utila.file_remove(info_path)  # remove old one to replace with new one
    link.dump_job(info_path, info)


def jobid(path: str) -> int:
    info_path = os.path.join(path, link.JOB_FILE_NAME)
    assert os.path.exists(info_path), str(info_path)
    info = link.load_job(info_path)
    return info.index
