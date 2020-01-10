# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Load different recipes from this package."""
import os
import typing

import rawmaker.cli as cli
import utila
import utila.test

DECIDER_FONTS = 'decider_fonts'
FEED_DECIDER_BORDER = 'feedback_decider_border'
FEED_DECIDER_FONTS = 'feedback_decider_fonts'
GROUPME = 'groupme'
SECTIONS = 'sections'
WORDS = 'words'
FEEDBACK = 'feedback'
RAWMAKER_OUTPUT = 'rawmaker'

COMMON_VIEW_WORK = 'commonview'


def run(
        runnable: str,
        inpath: typing.List[str],
        outpath: str = None,
        parameter: str = None,
        prefix: str = '',
        **kwargs,
):
    if isinstance(inpath, str):
        inpath = [inpath]
    for item in inpath:
        assert os.path.exists(item), item

    if prefix:
        prefix = '--prefix ' + prefix

    cmds = ['--%s %s' % (param, value) for (param, value) in kwargs.items()]
    cmds = ' '.join(cmds)
    # single inputpath does not produces -i, see str.join docu
    inputpath = ' -i '.join(inpath)

    parameter = ' ' if parameter is None else parameter
    command = '%s %s -i %s -o %s %s %s' % (
        runnable,
        parameter,
        inputpath,
        outpath,
        prefix,
        cmds,
    )
    utila.log('running: %s' % command)
    completed = utila.test.run(command)

    utila.log(completed.stdout)
    assert completed.returncode == utila.SUCCESS, completed.stdout + completed.stderr
    assert os.path.exists(outpath)

    return completed.returncode


CHAR_MARGIN_DEFAULT = float(cli.CHAR_MARGIN.defaultvar)
BOXES_FLOW_DEFAULT = float(cli.BOXES_FLOW.defaultvar)


def rawmaker(
        inpath: str,
        outpath: str = None,
        prefix='',
        char_margin: float = CHAR_MARGIN_DEFAULT,
        boxes_flow: float = BOXES_FLOW_DEFAULT,
        **kwargs,
) -> int:
    """Run external rawmaker

    Args:
        workspace(str): working path were input/output is relativ
        inpath(str): relative input path
        outpath(str): relative output path
        prefix(str): to extend the output name with a prefix
        kwargs(dict):
    Returns:
        0 if process succeeded else failure code
    """
    if isinstance(inpath, str):
        inpath = [inpath]
    kwargs[cli.CHAR_MARGIN.name] = char_margin
    kwargs[cli.BOXES_FLOW.name] = boxes_flow
    returncode = run(
        'rawmaker',
        inpath,
        outpath,
        '-j=8',
        prefix,
        **kwargs,
    )
    return returncode


def groupme(inpath: str, output: str = None):
    run('groupme', inpath, output)


def detector(inpath: str, outpath: str = None):
    run('detector', inpath, outpath)


def detector_titlepage(inpath: str, outpath: str = None):
    run('detector --titlepage', inpath, outpath)


def decider_titlepage(inpath: str, output: str = None):
    run('decider --titlepage', inpath, output)


def decider_toc(inpath: str, output: str = None):
    run('decider --toc', inpath, output)


def feedback_view(inpath: str, output: str = None):
    # TODO: Remove after feedview is working correctly
    missing_outdir = os.path.join(output, 'feedback__view_pages')
    os.makedirs(missing_outdir, exist_ok=True)
    run(f'{FEEDBACK} --view', inpath, output)


def determine_name(filepath):
    assert filepath, str(filepath)
    _, name = os.path.split(filepath)
    name = name.replace('.py', '')
    return name


RUNNER = [
    'analysis_statistica',
    'decider_border',
    'feedback',
    'feedback_decider_border',
    'feedback_statistica',
    'groupme',
    'rawmaker',
]


def check(workspace: str):
    ret = 0
    for item in RUNNER:
        utila.log(' check %s ' % item, end='')
        result = utila.test.run('%s --version' % item, workspace)
        utila.log(result.stdout.strip())
        if result.returncode:
            utila.error('Could not run %s' % item)
            utila.error(str(result))
        ret += result.returncode
    if ret:
        exit(ret)
    utila.log()  # add newline


def assert_validdocument(document: str):
    """Accepted chars are character, numbers and underscore."""
    valid = [item.isalnum() or item == '_' for item in document]
    assert all(valid), str(document)  # ensure to pass no path
