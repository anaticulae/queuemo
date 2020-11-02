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

import utila
import utila.cli

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
            outputparameter=True,
        ),
        prog='queuemo_single',
        version=queuemo.__version__,
    )
    args = utila.parse(parser)
    inpath, outpath = utila.sources(args, singleinput=True)
    if os.path.isfile(inpath):
        utila.error(f'require directory: {inpath}')
        exit(utila.INVALID_COMMAND)

    os.makedirs(outpath, exist_ok=True)
    utila.log(f'write result to: {outpath}')
    jobid = queuemo.worker.startup.jobid(inpath)
    queuemo.runtime.execute.run_document(inpath, jobid, outpath=outpath)
