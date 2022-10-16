# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import signal
import sys

import link
import utila

STOPPED = False
CURRENT = None


def isrunning():
    return not isstoped()


def isstoped() -> bool:
    return STOPPED


def stop():
    utila.log('\n\nstop service')
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
        sys.exit(utila.SUCCESS)
        return
    # TODO: MARK JOB AS TODO? AND RESTART LATER?
    utila.error(f'fail: {current}')
    link.fail(current, 'SCHEDULER SHUTDOWN')
    sys.exit(utila.SUCCESS)


# configure close handler
if utila.iswin():
    # TODO: INVESTIGATE LINUX
    signal.signal(signal.SIGBREAK, shutdown)  # pylint:disable=E1101
if not utila.testing():
    # TODO: ENSURE TO RUN IN MAIN THREAD, AFTER THIS WE CAN REMOVE TESTING CHECK
    signal.signal(signal.SIGINT, failcurrent)
