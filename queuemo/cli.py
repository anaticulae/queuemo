# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila
import utila.cli

import queuemo
import queuemo.worker.scheduler

PROCESS_NAME = 'queuemo'
RUNTIME = 'runtime'
WAITING = 'waiting'
VERBOSE = 'verbose'

COMMANDS = [
    utila.Parameter(
        longcut=RUNTIME,
        message='runtime in seconds',
        args={
            'default': 1,
        },
    ),
    utila.Parameter(
        longcut=WAITING,
        message='time to wait for the next job in miliseconds',
        args={
            'default': 1000,
        },
    ),
]


@utila.saveme
def main():
    parser = utila.cli.create_parser(
        todo=COMMANDS,
        prog=PROCESS_NAME,
        version=queuemo.__version__,
        verboseflag=True,
    )
    args = utila.parse(parser)
    try:
        runtime, waiting = int(args[RUNTIME]), int(args[WAITING])
        verbose = int(args[VERBOSE]) if args[VERBOSE] else 0
        utila.level_setup(verbose)
    except ValueError:
        msg = 'invalid start parameter: `%s`, `%s`, `%s`'
        utila.error(msg % (args[RUNTIME], args[WAITING], args[VERBOSE]))
        return utila.INVALID_COMMAND
    configo.check_startup()
    # start scheduler
    closed = queuemo.worker.scheduler.run(
        runtime=runtime,
        waiting=waiting,
        verbose=verbose,
    )

    return closed
