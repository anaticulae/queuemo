# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Load different recipes from this package."""
from functools import partial
from os.path import exists
from os.path import join
from os.path import split
from typing import List

from rawmaker.cli import BOXES_FLOW
from rawmaker.cli import CHAR_MARGIN
from utila import SUCCESS
from utila import copy_content
from utila import error
from utila import log
from utila.test import run as _run_target

from queuemo import ROOT
from queuemo.tabstructure import load as load_tabstructure

PDF_FILE = '../work.pdf'

DECIDER_FONTS = 'decider_fonts'
FEED_DECIDER_BORDER = 'feedback_decider_border'
FEED_DECIDER_FONTS = 'feedback_decider_fonts'
GROUPME = 'groupme'
SECTIONS = 'sections'
WORDS = 'words'
FEEDBACK = 'feedback'
RAWMAKER_OUTPUT = 'rawmaker'

COMMON_VIEW_WORK = 'commonview'

LAYOUT_PATH = join(ROOT, 'queuemo/layout.tab')
assert exists(LAYOUT_PATH), str(LAYOUT_PATH)
OUTPUT_LAYOUT = load_tabstructure(LAYOUT_PATH)


def run(
        runnable: str,
        workspace: str,
        inpath: List[str],
        outpath: str = None,
        parameter: str = None,
        prefix: str = '',
        **kwargs,
):
    if isinstance(inpath, str):
        inpath = [inpath]
    inputpath = [join(workspace, item) for item in inpath]
    for item in inputpath:
        assert exists(item), item

    if outpath is None:
        outputpath = join(workspace, runnable)
    else:
        outputpath = join(workspace, outpath)

    if prefix:
        prefix = '--prefix ' + prefix

    process = partial(_run_target, cwd=workspace)
    cmds = ['--%s %s' % (param, value) for (param, value) in kwargs.items()]
    cmds = ' '.join(cmds)
    # single inputpath does not produces -i, see str.join docu
    inputpath = ' -i '.join(inputpath)

    parameter = ' ' if parameter is None else parameter
    command = '%s %s -i %s -o %s %s %s' % (
        runnable,
        parameter,
        inputpath,
        outputpath,
        prefix,
        cmds,
    )
    log('running: %s' % command)
    completed = process(command)

    log(completed.stdout)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr
    assert exists(outputpath)

    return completed.returncode


CHAR_MARGIN_DEFAULT = float(CHAR_MARGIN.defaultvar)
BOXES_FLOW_DEFAULT = float(BOXES_FLOW.defaultvar)


def rawmaker(
        workspace: str,
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
    kwargs[CHAR_MARGIN.name] = char_margin
    kwargs[BOXES_FLOW.name] = boxes_flow
    returncode = run(
        'rawmaker',
        workspace,
        inpath,
        outpath,
        '-j=4',
        prefix,
        **kwargs,
    )
    return returncode


def analysis_statistica(workspace: str, inputs: str, output: str = None):
    run('analysis_statistica', workspace, inputs, output)


def groupme(workspace: str, inputs: str, output: str = None):
    run('groupme', workspace, inputs, output)


def sections(workspace: str, inputs: str, output: str = None):
    run(
        SECTIONS,
        workspace,
        inputs,
        output,
        parameter='-j=4',
    )


def feedback_analysis_statistica(
        workspace: str,
        input_: List[str],
        output: str = None,
):
    run('feedback_statistica', workspace, input_, output)


def detector(workspace: str, input_: str, output: str = None):
    run('detector', workspace, input_, output)


def decider_decider(workspace: str, input_: str, output: str = None):
    run('decider', workspace, input_, output)


def decider_titlepage(workspace: str, input_: str, output: str = None):
    run('decider --titlepage', workspace, input_, output)


def decider_toc(workspace: str, input_: str, output: str = None):
    run('decider --toc', workspace, input_, output)


def decider_border(workspace: str, input_: str, output: str = None):
    run('decider_border', workspace, input_, output)


def decider_fonts(workspace: str, input_: str, output: str = None):
    run(DECIDER_FONTS, workspace, input_, output)


def feedback_decider_border(workspace: str, input_: str, output: str = None):
    run(FEED_DECIDER_BORDER, workspace, input_, output)


def feedback_decider_fonts(workspace: str, input_: str, output: str = None):
    run(FEED_DECIDER_FONTS, workspace, input_, output)


def words(workspace: str, input_: str, output: str = None):
    run(WORDS, workspace, input_, output, parameter='-j=4')


def feedback(workspace: str, input_: str, output: str = None):
    run(FEEDBACK, workspace, input_, output)


def feedback_view(workspace: str, inpath: str, output: str = None):
    run(f'{FEEDBACK} --view', workspace, inpath, output)


def copy(workspace: str, input_: str, output: str):
    inputpath = join(workspace, input_)
    outputpath = join(workspace, output) if output is not None else inputpath

    assert exists(inputpath), inputpath

    copy_content(inputpath, outputpath, recursive=True)


def publish(rawspace: str, input_: str, output: str):
    # TODO: add method publish_html, publish_image?
    return
    output = OUTPUT_LAYOUT.look(output)
    output = join('../result', output)

    inputpath = join(rawspace, input_)

    output = join(output, 'index.html')
    outputpath = join(rawspace, output)

    assert exists(inputpath), inputpath

    copy_content(inputpath, outputpath, recursive=True)


# TODO: Make defining publishing structure easier, see below
# statistica:6
#     chapter:5
#         words:4


def determine_name(filepath):
    assert filepath, str(filepath)
    _, name = split(filepath)
    name = name.replace('.py', '')
    return name


RUNNER = [
    'analysis_statistica',
    'decider_border',
    'feedback_decider_border',
    # 'feedback_statistica',
    'groupme',
    'rawmaker',
]


def check(workspace: str):
    ret = 0
    for item in RUNNER:
        log(' check %s ' % item, end='')
        result = _run_target('%s --version' % item, workspace)
        log(result.stdout.strip())
        if result.returncode:
            error('Could not run %s' % item)
            error(str(result))
        ret += result.returncode
    if ret:
        exit(ret)
    log()  # add newline


def assert_validdocument(document: str):
    assert document.isalnum(), str(document)  # ensure to pass no path
