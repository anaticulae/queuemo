# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import signal
import sys

import link
import utila

STOPED = False
CURRENT = None


def isrunning():
    return not isstoped()


def isstoped() -> bool:
    return STOPED


def stop():
    utila.log('\n\nstop service')
    global STOPED  # pylint:disable=global-statement
    STOPED = True


def shutdown(event, action):  # pylint:disable=W0613
    """Use CTRL+BREAK to close scheduler softly."""
    stop()


def set_current(job: int = None):
    global CURRENT  # pylint:disable=global-statement
    CURRENT = job


def current_job():
    global CURRENT  # pylint:disable=global-statement
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
signal.signal(signal.SIGBREAK, shutdown)
signal.signal(signal.SIGINT, failcurrent)
