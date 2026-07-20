# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import configos
import link
import serializeraw
import utilo
import utilo.cli

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


@utilo.saveme
def main():
    config = evaluate_cli()
    if config == utilo.INVALID_COMMAND:
        return utilo.INVALID_COMMAND
    # run showdebug
    if config.showdebug:
        return showdebug()
    configure(config)
    closed = worker_startup(config)
    return closed


def configure(config: Config):
    queuemo.INTERACTIVE = config.interactive
    queuemo.cli.utils.logger_start()
    if config.interactive:
        utilo.log('use interactive mode')
    if not utilo.testing():
        # ensure that all test directories are created
        configos.makedirs()
    # check startup
    configos.check_startup()
    if config.clean:
        # remove outdated maybe failed jobs
        link.remove_outdated()
    # run http interface if required
    if config.http:
        http_startup()


def worker_startup(config: Config):
    # start scheduler
    import queuemo.worker.startup  # pylint:disable=W0621,C0415
    closed = queuemo.worker.startup.run(
        failfast=config.failfast,
        jobs=config.jobs,
        runtime=config.runtime,
        skip_unsupported=config.skip_unsupported,
        verbose=config.verbose,
        waiting=config.waiting,
        webconfig=config.webconfig,
    )
    return closed


def http_startup():
    # lower queuemo start time, flask requires a second of init time
    import queuemo.runtime.control  # pylint:disable=W0621,C0415
    queuemo.runtime.control.start()


CMDS = [
    utilo.Parameter(
        longcut=RUNTIME,
        message='runtime in ticks',
        args={
            'default': 100,
        },
    ),
    utilo.Parameter(
        longcut=WAITING,
        message='time to wait for the next job in miliseconds',
        args={
            'default': 1000,
        },
    ),
    utilo.Parameter(
        longcut=JOBS,
        message='maximal number of executed jobs',
        args={
            'default': 1000,
        },
    ),
    utilo.Flag(
        longcut=INTERACTIVE,
        message='pause on every recipe step and ask to continue',
    ),
    utilo.Flag(
        longcut='failfast',
        message='fail on first error',
    ),
    utilo.Flag(
        longcut='http',
        message='start http interface',
    ),
    utilo.Flag(
        longcut='showdebug',
        message='show list of installed runnable and return',
    ),
    utilo.Flag(
        longcut='clean',
        message='clean outdated jobs',
    ),
    utilo.Flag(
        longcut='skip_unsupported',
        message='do not analyze not supported documents',
    ),
    utilo.Parameter(
        longcut='webconfig',
        message='select msgids of published findings',
    ),
]


def evaluate_cli() -> Config:
    parser = utilo.cli.create_parser(
        todo=CMDS,
        config=utilo.ParserConfiguration(
            waitingflag=False,
            cacheflag=False,
            pages=False,
        ),
        prog=queuemo.PROCESS,
        version=queuemo.__version__,
    )
    args = utilo.parse(parser)
    try:
        webconfig = args.get('webconfig', None)
        if webconfig:
            if not utilo.exists(webconfig):
                utilo.error(f'webconfig does not exists: {webconfig}')
                return utilo.INVALID_COMMAND
            utilo.debug(f'use webconfig: {webconfig}')
            webconfig = serializeraw.load_webconfig(webconfig)
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
            webconfig=webconfig,
        )
    except ValueError:
        msg = (f'invalid start parameter: `{args[RUNTIME]}`, `{args[WAITING]}`,'
               f' `{args[VERBOSE]}`, `{args[JOBS]}`')
        utilo.error(args)
        utilo.error(msg)
        return utilo.INVALID_COMMAND
    utilo.level_setup(config.verbose)
    return config


def showdebug():
    queuemo.runnable.check()
    return utilo.SUCCESS
