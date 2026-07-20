# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import signal
import sys

import link
import utilo

STOPPED = False
CURRENT = None


def isrunning():
    return not isstoped()


def isstoped() -> bool:
    return STOPPED


def stop():
    utilo.log('\n\nstop service')
    global STOPPED  # pylint:disable=global-statement
    STOPPED = True


def shutdown(event, action):  # pylint:disable=W0613
    """Use CTRL+BREAK to close scheduler softly."""
    stop()


def set_current(job: int = None):
    global CURRENT  # pylint:disable=global-statement
    CURRENT = job


def current_job():
    return CURRENT


def failcurrent(event, action):  # pylint:disable=W0613
    # close scheduler immediately and mark current analysis as failed
    current = current_job()
    stop()
    if not current:
        # nothing todo
        sys.exit(utilo.SUCCESS)
        return
    # TODO: MARK JOB AS TODO? AND RESTART LATER?
    utilo.error(f'fail: {current}')
    link.fail(current, 'SCHEDULER SHUTDOWN')
    sys.exit(utilo.SUCCESS)


# configure close handler
if utilo.iswin():
    # TODO: INVESTIGATE LINUX
    signal.signal(signal.SIGBREAK, shutdown)  # pylint:disable=E1101
if not utilo.testing():
    # TODO: ENSURE TO RUN IN MAIN THREAD, AFTER THIS WE CAN REMOVE TESTING CHECK
    signal.signal(signal.SIGINT, failcurrent)
