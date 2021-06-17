# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila
import utila.cli
import utila.logger

import queuemo
import queuemo.runtime.control
import queuemo.worker.startup

PROCESS_NAME = 'queuemo'
RUNTIME = 'runtime'
WAITING = 'waiting'
JOBS = 'jobs'
VERBOSE = 'verbose'
INTERACTIVE = 'interactive'

COMMANDS = [
    utila.Parameter(
        longcut=RUNTIME,
        message='runtime in ticks',
        args={
            'default': 100,
        },
    ),
    utila.Parameter(
        longcut=WAITING,
        message='time to wait for the next job in miliseconds',
        args={
            'default': 1000,
        },
    ),
    utila.Parameter(
        longcut=JOBS,
        message='maximal number of executed jobs',
        args={
            'default': 1000,
        },
    ),
    utila.Flag(
        longcut=INTERACTIVE,
        message='pause on every recipe step and ask to continue',
    ),
    utila.Flag(
        longcut='failfast',
        message='fail on first error',
    ),
    utila.Flag(
        longcut='http',
        message='start http interface',
    ),
]


@utila.saveme
def main():
    logger_start()
    parser = utila.cli.create_parser(
        todo=COMMANDS,
        config=utila.ParserConfiguration(verboseflag=True),
        prog=PROCESS_NAME,
        version=queuemo.__version__,
    )
    args = utila.parse(parser)
    queuemo.INTERACTIVE = args[INTERACTIVE]
    failfast = args.get('failfast', False)
    if queuemo.INTERACTIVE:
        utila.log('use interactive mode')
    try:
        runtime, waiting = int(args[RUNTIME]), int(args[WAITING])
        jobsleft = int(args[JOBS])
        verbose = int(args[VERBOSE]) if args[VERBOSE] else 0
        utila.level_setup(verbose)
    except ValueError:
        msg = (f'invalid start parameter: `{args[RUNTIME]}`, `{args[WAITING]}`,'
               f' `{args[VERBOSE]}`, `{args[JOBS]}`')
        utila.error(msg)
        return utila.INVALID_COMMAND
    configo.check_startup()

    if args['http']:
        queuemo.runtime.control.start()
    # start scheduler
    closed = queuemo.worker.startup.run(
        runtime=runtime,
        waiting=waiting,
        jobs=jobsleft,
        verbose=verbose,
        failfast=failfast,
    )
    return closed


def logger_start():
    tmp = configo.tmp(True)
    logfile = f'{utila.filetime()}_{utila.tmpname(10)}.log'
    outpath = os.path.join(tmp, logfile)
    # do not write logger command when using --help or --version
    utila.debug(f'write global log to {outpath}')
    utila.logger.OUTFILE = outpath
