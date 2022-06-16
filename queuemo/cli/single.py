# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Run queuemo for selected pdf file."""

import os

import configo
import link
import utila
import utila.cli
import utila.logger

import queuemo
import queuemo.cli.utils
import queuemo.runtime.api
import queuemo.runtime.execute
import queuemo.worker.startup

COMMANDS = [
    utila.Flag(longcut='create'),
]
DESCRIPTION = """\
Run queuemo recipe for given -i input and write to -o folder.
"""


@utila.saveme
def main() -> int:
    inpath, outpath, verbose, create = eval_cli()
    utila.logger.level_setup(utila.Level(verbose))
    queuemo.cli.utils.logger_start()
    if os.path.isfile(inpath):
        if create:
            inpath = create_todo(inpath, outpath)
            if inpath == utila.FAILURE:
                return utila.FAILURE
        else:
            utila.error(f'require directory: {inpath} or use --create flag')
            return utila.INVALID_COMMAND
    outpath = inpath
    utila.log(f'write result to: {outpath}')
    # patch todo outpath path. TODO: INVESTIGATE HERE?
    todopath = os.path.normpath(os.path.join(inpath, os.path.pardir))
    configo.todo = lambda _=False: todopath
    configo.ready = lambda _=False: todopath
    # analyze single document
    tmpdir = utila.tmpdir(configo.tmp())
    jobid = queuemo.worker.startup.jobid(inpath)
    queuemo.runtime.execute.run_document(
        workspace=tmpdir,
        documentid=jobid,
        outpath=outpath,
        config=queuemo.runtime.api.RecipeConfig(verbose=verbose),
    )
    return utila.SUCCESS


def eval_cli() -> tuple:
    parser = utila.cli.create_parser(
        description=DESCRIPTION,
        todo=COMMANDS,
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=True,
        ),
        prog='queuemo_single',
        version=queuemo.__version__,
    )
    args = utila.parse(parser)
    inpath, outpath, verbose = utila.sources(  # pylint:disable=W0632
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
        utila.error(f'{os.path.join(outpath, outname)} already exists')
        return utila.FAILURE
    utila.log(f'create job description in {outpath}')
    return outpath
