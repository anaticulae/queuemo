# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os

import configo
import link
import utila
import utila.cli
import utila.logger

import queuemo
import queuemo.runnable
import queuemo.runtime.control
import queuemo.worker.startup

RUNTIME = 'runtime'
WAITING = 'waiting'
JOBS = 'jobs'
VERBOSE = 'verbose'
INTERACTIVE = 'interactive'

CMDS = [
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
    utila.Flag(
        longcut='showdebug',
        message='show list of installed runnable and return',
    ),
]

Config = collections.namedtuple(
    'Config',
    'interactive failfast showdebug runtime waiting jobs verbose http',
)


def evaluate_cli() -> Config:
    parser = utila.cli.create_parser(
        todo=CMDS,
        config=utila.ParserConfiguration(),
        prog=queuemo.PROCESS,
        version=queuemo.__version__,
    )
    args = utila.parse(parser)
    try:
        config = Config(
            args[INTERACTIVE],
            args.get('failfast', False),
            args.get('showdebug', False),
            int(args[RUNTIME]),
            int(args[WAITING]),
            int(args[JOBS]),
            int(args[VERBOSE]) if args[VERBOSE] else 0,
            args['http'],
        )
    except ValueError:
        msg = (f'invalid start parameter: `{args[RUNTIME]}`, `{args[WAITING]}`,'
               f' `{args[VERBOSE]}`, `{args[JOBS]}`')
        utila.error(msg)
        return utila.INVALID_COMMAND
    utila.level_setup(config.verbose)
    return config


@utila.saveme
def main():
    config = evaluate_cli()
    if config == utila.INVALID_COMMAND:
        return utila.INVALID_COMMAND
    # run showdebug
    if config.showdebug:
        return showdebug()
    queuemo.INTERACTIVE = config.interactive
    logger_start()
    if config.interactive:
        utila.log('use interactive mode')
    # check startup
    configo.check_startup()
    # remove outdated maybe failed jobs
    link.remove_outdated()
    # run http interface if required
    if config.http:
        queuemo.runtime.control.start()
    # start scheduler
    closed = queuemo.worker.startup.run(
        runtime=config.runtime,
        waiting=config.waiting,
        jobs=config.jobs,
        verbose=config.verbose,
        failfast=config.failfast,
    )
    return closed


def logger_start():
    tmp = configo.tmp(True)
    # create log folder
    queuemo_tmp = os.path.join(tmp, 'queuemo/log/')
    os.makedirs(queuemo_tmp, exist_ok=True)
    # determine current file name
    logfile = f'{utila.filetime()}_{utila.tmpname(10)}.log'
    outpath = os.path.join(queuemo_tmp, logfile)
    # do not write logger command when using --help or --version XXX???
    utila.debug(f'write global log to {outpath}')
    utila.logger.OUTFILE = outpath


def showdebug():
    queuemo.runnable.check()
    return utila.SUCCESS
