# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Run queuemo for selected pdf file."""

import os

import configos
import link
import utilo
import utilo.cli
import utilo.logger

import queuemo
import queuemo.cli.utils
import queuemo.runtime.api
import queuemo.runtime.execute
import queuemo.worker.startup

COMMANDS = [
    utilo.Flag(longcut='create'),
]
DESCRIPTION = """\
Run queuemo recipe for given -i input and write to -o folder.
"""


@utilo.saveme
def main() -> int:
    inpath, outpath, verbose, create = eval_cli()
    utilo.logger.level_setup(utilo.Level(verbose))
    queuemo.cli.utils.logger_start()
    if os.path.isfile(inpath):
        if create:
            inpath = create_todo(inpath, outpath)
            if inpath == utilo.FAILURE:
                return utilo.FAILURE
        else:
            utilo.error(f'require directory: {inpath} or use --create flag')
            return utilo.INVALID_COMMAND
    outpath = inpath
    utilo.log(f'write result to: {outpath}')
    # patch todo outpath path. TODO: INVESTIGATE HERE?
    todopath = os.path.normpath(os.path.join(inpath, os.path.pardir))
    configos.todo = lambda _=False: todopath
    configos.ready = lambda _=False: todopath
    # analyze single document
    tmpdir = utilo.tmpdir(configos.tmp())
    jobid = queuemo.worker.startup.jobid(inpath)
    queuemo.runtime.execute.run_document(
        workspace=tmpdir,
        documentid=jobid,
        outpath=outpath,
        config=queuemo.runtime.api.RecipeConfig(verbose=verbose),
    )
    return utilo.SUCCESS


def eval_cli() -> tuple:
    parser = utilo.cli.create_parser(
        description=DESCRIPTION,
        todo=COMMANDS,
        config=utilo.ParserConfiguration(
            inputparameter=True,
            outputparameter=True,
        ),
        prog='queuemo_single',
        version=queuemo.__version__,
    )
    args = utilo.parse(parser)
    inpath, outpath, verbose = utilo.sources(  # pylint:disable=W0632
        args,
        singleinput=True,
        use_cwd=False,
        verbose=True,
    )
    inpath = inpath[0]
    create = args.get('create', False)
    return inpath, outpath, verbose, create


def create_todo(inpath, outpath):
    filename = str(os.path.split(inpath)[1])
    if outpath:
        outpath, outname = os.path.split(outpath)
    else:
        outpath = os.getcwd()
        # remove file name
        outname = filename.replace('.pdf', '')
    try:
        outpath = link.create_todo(
            file=inpath,
            filename=filename,
            todoname=outname,
            todopath=outpath,
            exist_ok=True,
        )
    except OSError:
        utilo.error(f'{os.path.join(outpath, outname)} already exists')
        return utilo.FAILURE
    utilo.log(f'create job description in {outpath}')
    return outpath
