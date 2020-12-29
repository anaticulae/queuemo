# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Run queuemo for selected pdf file."""

import os

import configo
import utila
import utila.cli
import utila.logger

import queuemo
import queuemo.runtime.execute
import queuemo.worker.startup

COMMANDS = []
DESCRIPTION = """\
Run queuemo recipe for given -i input and write to -o folder.
"""


@utila.saveme
def main() -> int:
    parser = utila.cli.create_parser(
        description=DESCRIPTION,
        todo=COMMANDS,
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=False,
        ),
        prog='queuemo_single',
        version=queuemo.__version__,
    )
    args = utila.parse(parser)
    inpath, _, verbose = utila.sources(
        args,
        singleinput=True,
        use_cwd=False,
        verbose=True,
    )
    utila.logger.level_setup(utila.Level(verbose))
    inpath = inpath[0]
    if os.path.isfile(inpath):
        utila.error(f'require directory: {inpath}')
        return utila.INVALID_COMMAND
    outpath = inpath

    # patch todo output path. TODO: INVESTIGATE HERE?
    todopath = os.path.normpath(os.path.join(inpath, os.path.pardir))
    configo.todo = lambda _=False: todopath
    configo.ready = lambda _=False: todopath

    utila.log(f'write result to: {outpath}')

    tmpdir = utila.tmpdir(configo.tmp())
    jobid = queuemo.worker.startup.jobid(inpath)
    queuemo.runtime.execute.run_document(
        workspace=tmpdir,
        documentid=jobid,
        outpath=outpath,
    )
    return utila.SUCCESS
