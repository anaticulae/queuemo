# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from configo import check_startup
from utila import SUCCESS
from utila import Flag
from utila import Parameter
from utila import create_parser
from utila import parse
from utila import saveme

from queuemo import __version__
from queuemo.worker.scheduler import run as start_scheduler

PROCESS_NAME = 'queuemo'
RUNTIME = 'runtime'
WAITING = 'waiting'
VERBOSE = 'verbose'

COMMANDS = [
    Parameter(
        longcut=RUNTIME,
        message='runtime in seconds',
        args={'default': 1},
    ),
    Parameter(
        longcut=WAITING,
        message='waitime in miliseconds for next job',
        args={'default': 1000},
    ),
    Flag(
        args={'action': 'count'},
        longcut=VERBOSE,
        message='define how verbose logging is',
        shortcut='V',
    ),
]


@saveme
def main():
    parser = create_parser(
        todo=COMMANDS,
        prog=PROCESS_NAME,
        version=__version__,
    )
    args = parse(parser)
    runtime = int(args[RUNTIME])
    waiting = int(args[WAITING])
    verbose = int(args[VERBOSE]) if args[VERBOSE] else 0

    # TODO: Add verbose mechanismn to utila
    check_startup()  # TODO: Add verbose flag
    start_scheduler(runtime=runtime, waiting=waiting, verbose=verbose)

    return SUCCESS
