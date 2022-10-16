# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Watchdog of todo folder to listen for incoming jobs."""

import os
import time

import configo
import iamraw
import link
import utila

import queuemo
import queuemo.runtime.api
import queuemo.runtime.execute
import queuemo.runtime.status

MAX_RUNTIME = 60 * 60 * 24 * 365  # Run one year
WAITING = 1000  # ms, 1 second
JOBSLEFT = 1000


def run(
    runtime: float = MAX_RUNTIME,
    waiting: float = WAITING,
    jobs: int = JOBSLEFT,
    failfast: bool = False,
    skip_unsupported: bool = False,
    webconfig: iamraw.WebConfig = None,
    verbose: bool = True,
) -> int:
    """Run the scheduler

    Args:
        runtime(float): runtime in seconds
        waiting(float): waiting time in mili-seconds
        jobs(int): maximal number of executed jobs, decrease for every
                   step and stop if no jobs are left.
        failfast(bool): shut down on first failure
        skip_unsupported(bool): do not analyze unsupported documents
        webconfig(WebConfig): select published findingids
        verbose(bool): increase logging if True
    Returns:
        SUCCESS when scheduler ends, or Exception, when runtime error occurs
    """
    todopath = configo.todo(True)
    config = queuemo.runtime.api.RecipeConfig(
        failfast=failfast,
        skip_unsupported=skip_unsupported,
        webconfig=webconfig,
        verbose=verbose,
    )
    utila.log(f'start working on: {todopath}')
    utila.print_env()
    if not waiting:
        waiting = 1
    tick = 0
    while tick < runtime and jobs > 0:  # pylint:disable=W0149
        if queuemo.runtime.status.isstoped():
            utila.log('service is stopped, stop working')
            break
        job = nextjob()
        try:
            if job is not None:
                jobs -= 1
                utila.log(f'\njobs remaining: {jobs}')
            step(
                job,
                waiting=waiting,
                config=config,
            )
        except Exception:  # pylint: disable=broad-except
            utila.log_stacktrace()
            utila.error(f'\nClose scheduler: {tick}')
            return utila.FAILURE
        tick += 1
        if not verbose and tick % 80 == 0:  # pylint:disable=C2001
            utila.log()  # write newline
    utila.log(f'\nTerminated: {tick}')
    return utila.SUCCESS


def step(
    job: int,
    config: queuemo.runtime.api.RecipeConfig,
    waiting=WAITING,
):
    if not job:
        if config.verbose:
            utila.log('Wait...')
        else:
            utila.log('.', end='')
        time.sleep(waiting / 1000)  # miliseconds to seconds
        return
    # execute jobs steps
    if not config.verbose:
        utila.log()  # write newline
    utila.log('Run job')
    queuemo.runtime.status.set_current(job)
    if config.verbose:
        utila.log('  Copy job')
    # copy
    workspace = copy(job)
    if config.verbose:
        utila.log('  Start job')
    with utila.profile(workspace):
        work(workspace, config=config)
    if config.verbose:
        utila.log('Finished')
    queuemo.runtime.status.set_current(None)


def nextjob() -> int:
    """Find next job and mark it as `in progress`.

    1. Select the todo folder and search for a folder that does not include
       an `inprogress` file.
    2. After finding an waiting job, start them and return the `jobid`
       as nextjob. (TODO: START IS NOT DONE HERE)

    Scheduler(current): use first waiting job. The order is randomly
        selected by file-name of tmp-job cause os.listdir selects folder in
        arbitrary order and the document length and document folder name
        does not correspondent with each other.
    Scheduler(planned): TODO: make scheduler page length dependent?

    Returns:
        If there is a matching file, return the folder name as jobid
        If there is no matching file, return `None`
    """
    # TODO: INTRODUCE MORE USERFRIENDLY SCHEDULER, RUN SHORT DOCS FIRST?
    todopath = configo.todo(True)
    for jobnumber in os.listdir(todopath):
        itempath = os.path.join(todopath, jobnumber)
        if os.path.isfile(itempath):
            # require input folder, not a single file
            utila.error(f'file: not a input resource: {itempath}')
            continue
        if link.inprogressed(jobnumber):
            continue
        if link.deleted(jobnumber):
            continue
        if link.failed(jobnumber):
            continue
        # return next job, start it by recipe runner
        return jobnumber
    return None


def copy(job):
    """Copy job to temporary workspace folder."""
    path = os.path.join(configo.todo(), job)
    assert os.path.exists(path), str(path)
    # determine tmporary folder and copy todo
    workspace = utila.tmpfile(queuemo.ROOT)
    # copy todo to temporary folder
    utila.copy_content(
        src=path,
        dst=workspace,
        recursive=True,
        unlock=True,
    )
    return workspace


def work(workspace, config):
    assert os.path.exists(workspace), str(workspace)
    current = jobid(workspace)
    outpath = os.path.join(configo.todo(), current)

    queuemo.runtime.execute.run_document(
        workspace,
        documentid=jobid(workspace),
        outpath=outpath,
        config=config,
    )


def jobid(path: str) -> int:
    info_path = os.path.join(path, link.JOB_FILE_NAME)
    assert os.path.exists(info_path), str(info_path)
    info = link.load_job(info_path)
    return info.name
