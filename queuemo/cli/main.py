# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import configo
import link
import serializeraw
import utila
import utila.cli

import queuemo
import queuemo.cli.utils
import queuemo.runnable

RUNTIME = 'runtime'
WAITING = 'waiting'
JOBS = 'jobs'
VERBOSE = 'verbose'
INTERACTIVE = 'interactive'

Config = collections.namedtuple(
    'Config',
    ('interactive failfast showdebug clean runtime waiting '
     'jobs verbose http skip_unsupported webconfig'),
)


@utila.saveme
def main():
    config = evaluate_cli()
    if config == utila.INVALID_COMMAND:
        return utila.INVALID_COMMAND
    # run showdebug
    if config.showdebug:
        return showdebug()
    # TODO: DONT KNOW WHY GLOBAL IS REQUIRED
    global queuemo  # pylint:disable=C0103,global-statement
    queuemo.INTERACTIVE = config.interactive
    queuemo.cli.utils.logger_start()
    if config.interactive:
        utila.log('use interactive mode')
    if not utila.testing():
        # ensure that all test directories are created
        configo.makedirs()
    # check startup
    configo.check_startup()
    if config.clean:
        # remove outdated maybe failed jobs
        link.remove_outdated()
    # run http interface if required
    if config.http:
        # lower queuemo start time, flask requires a second of init time
        import queuemo.runtime.control  # pylint:disable=W0621,C0415
        queuemo.runtime.control.start()
    webconfig = None
    if config.webconfig:
        if not utila.exists(config.webconfig):
            utila.error(f'webconfig does not exists: {config.webconfig}')
            return utila.INVALID_COMMAND
        utila.debug(f'use webconfig: {config.webconfig}')
        webconfig = serializeraw.load_webconfig(config.webconfig)
    # start scheduler
    import queuemo.worker.startup  # pylint:disable=C0415
    closed = queuemo.worker.startup.run(
        failfast=config.failfast,
        jobs=config.jobs,
        runtime=config.runtime,
        skip_unsupported=config.skip_unsupported,
        verbose=config.verbose,
        waiting=config.waiting,
        webconfig=webconfig,
    )
    return closed


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
    utila.Flag(
        longcut='clean',
        message='clean outdated jobs',
    ),
    utila.Flag(
        longcut='skip_unsupported',
        message='do not analyze not supported documents',
    ),
    utila.Parameter(
        longcut='webconfig',
        message='select msgids of published findings',
    ),
]


def evaluate_cli() -> Config:
    parser = utila.cli.create_parser(
        todo=CMDS,
        config=utila.ParserConfiguration(
            waitingflag=False,
            cacheflag=False,
            pages=False,
        ),
        prog=queuemo.PROCESS,
        version=queuemo.__version__,
    )
    args = utila.parse(parser)
    try:
        config = Config(
            args[INTERACTIVE],
            args.get('failfast', False),
            args.get('showdebug', False),
            args.get('clean', False),
            int(args[RUNTIME]),
            int(args[WAITING]),
            int(args[JOBS]),
            int(args[VERBOSE]) if args[VERBOSE] else 0,
            args.get('http', False),
            args.get('skip_unsupported', False),
            args.get('webconfig', None),
        )
    except ValueError:
        msg = (f'invalid start parameter: `{args[RUNTIME]}`, `{args[WAITING]}`,'
               f' `{args[VERBOSE]}`, `{args[JOBS]}`')
        utila.error(msg)
        return utila.INVALID_COMMAND
    utila.level_setup(config.verbose)
    return config


def showdebug():
    queuemo.runnable.check()
    return utila.SUCCESS
