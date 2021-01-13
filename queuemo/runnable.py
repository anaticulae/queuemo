# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Load different recipes from this package."""

import os

import rawmaker.cli as cli
import utila

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
        inpath: utila.Strings,
        outpath: str,
        parameter: str = None,
        prefix: str = '',
        **kwargs,
) -> int:
    if isinstance(inpath, str):
        inpath = [inpath]
    # beautify path: remove ../..
    outpath = os.path.normpath(outpath)
    inpath = [os.path.normpath(item) for item in inpath]
    for item in inpath:
        assert os.path.exists(item), item
    if prefix:
        prefix = '--prefix ' + prefix

    cmds = kwargs_to_parameter(kwargs)
    # single inputpath does not produces -i, see str.join docu
    inputpath = ' -i '.join(inpath)

    parameter = ' ' if parameter is None else parameter
    cmd = f'{runnable} {parameter} -i {inputpath} -o {outpath} {prefix} {cmds}'
    utila.log(f'running: {cmd}')
    with utila.profile():
        completed = utila.run(cmd)

    utila.log(completed.stdout)
    assert os.path.exists(outpath), str(outpath)
    return completed.returncode


def kwargs_to_parameter(args: dict) -> str:
    if not args:
        return ''
    cmds = []
    for param, value in args.items():
        if value is True:
            cmds.append(f'--{param}')
        elif value is False:
            continue
        else:
            cmds.append(f'--{param} {value}')
    result = ' '.join(cmds)
    return result


CHAR_MARGIN_DEFAULT = float(cli.CHAR_MARGIN.defaultvar)
BOXES_FLOW_DEFAULT = float(cli.BOXES_FLOW.defaultvar)


def rawmaker(
        inpath: str,
        outpath: str = None,
        prefix: str = '',
        char_margin: float = CHAR_MARGIN_DEFAULT,
        boxes_flow: float = BOXES_FLOW_DEFAULT,
        **kwargs,
) -> int:
    """Run external rawmaker.

    Args:
        inpath(str): relative input path
        outpath(str): relative output path
        prefix(str): to extend the output name with a prefix
        char_margin(float): maximal distance between two chars
        boxes_flow(float): ratio betwee horizontal and vertical analysis
        kwargs(dict): ???
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


def linero(inpath: str, output: str = None):
    return run('linero', inpath, output)


def spacestation(inpath: str, output: str = None, **kwargs):
    run('spacestation', inpath, output, **kwargs)


def groupme(inpath: str, output: str = None, **kwargs):
    run('groupme -j8', inpath, output, **kwargs)


def sections(inpath: str, output: str = None):
    run('sections -j8', inpath, output)


def words(inpath: str, output: str = None, **kwargs):
    run('words -j8', inpath, output, **kwargs)


def words_links(inpath: str, output: str = None, **kwargs):
    run('words --links', inpath, output, **kwargs)


def detector_formula(inpath: str, outpath: str, **kwargs):
    run('detector --formula', inpath, outpath, **kwargs)


def detector_titlepage(inpath: str, outpath: str = None, **kwargs):
    run('detector --titlepage', inpath, outpath, **kwargs)


def decider_titlepage(inpath: str, output: str = None):
    run('decider --titlepage', inpath, output)


def decider_toc(inpath: str, output: str = None):
    run('decider_toc', inpath, output)


def decider_footnote(inpath: str, output: str = None):
    run('decider_footnote', inpath, output)


def decider_imgfig(inpath: str, output: str = None):
    run('decider_imgfig', inpath, output)


def decider_border_detecion(inpath: str, output: str = None):
    run('decider_border --detection', inpath, output)


def decider_border_distance(inpath: str, output: str = None):
    run('decider_border --distance', inpath, output)


def textflow_alignment(inpath: str, output: str = None, **kwargs):
    run('textflow --alignment', inpath, output, **kwargs)


def textflow_lineending(inpath: str, output: str = None, **kwargs):
    run('textflow --lineending', inpath, output, **kwargs)


def textflow_wordspace(inpath: str, output: str = None, **kwargs):
    run('textflow --wordspace', inpath, output, **kwargs)


def textflow_quotes(inpath: str, output: str = None, **kwargs):
    run('textflow --quotation --blockquote', inpath, output, **kwargs)


def doctextstyle(inpath: str, output: str = None, **kwargs):
    run('doctextstyle', inpath, output, **kwargs)


def caption(inpath: str, output: str = None, **kwargs):
    run('caption', inpath, output, **kwargs)


def magic(inpath: str, output: str = None, **kwargs):
    run('magic', inpath, output, **kwargs)


def docref(inpath: str, output: str = None, **kwargs):
    run('docref', inpath, output, **kwargs)


def docref_bibliography(inpath: str, output: str = None, **kwargs):
    run('docref --bibliography', inpath, output, **kwargs)


def chapter(inpath: str, output: str = None, **kwargs):
    run('chapter', inpath, output, **kwargs)


def smarty(inpath: str, output: str = None, **kwargs):
    run('smarty', inpath, output, **kwargs)


def decider_smarty(inpath: str, output: str = None, **kwargs):
    run('decider_smarty', inpath, output, **kwargs)


def decider_bibliography(inpath: str, output: str = None, **kwargs):
    run('decider_bibliography', inpath, output, **kwargs)


def decider_chapter(inpath: str, output: str = None, **kwargs):
    run('decider_chapter', inpath, output, **kwargs)


def decider_textstyle_headlines(inpath: str, output: str = None, **kwargs):
    # TODO: Enable later; activate after utila supports selective inputs
    # run('decider_textflow --lineending', inpath, output)
    run('decider_textstyle --headlines', inpath, output, **kwargs)


def decider_textstyle_text(inpath: str, output: str = None, **kwargs):
    run('decider_textstyle --text', inpath, output, **kwargs)


def detector_bibliography(inpath: str, output: str = None, **kwargs):
    run('detector --bibliography', inpath, output, **kwargs)


def decider_links(inpath: str, output: str = None):
    run('decider --links', inpath, output)


def decider_textflow_lineending(inpath: str, output: str = None, **kwargs):
    # TODO: Enable later; activate after utila supports selective inputs
    # run('decider_textflow --lineending', inpath, output)
    run('decider_textflow', inpath, output, **kwargs)


def feedback_images(inpath: str, output: str = None):
    # TODO: Remove after feedview is working correctly
    missing_outdir = os.path.join(output, 'feedback__view_pages')
    os.makedirs(missing_outdir, exist_ok=True)
    run(f'{FEEDBACK} --images --figures', inpath, output)


def feedback_view(inpath: str, output: str = None):
    # TODO: Remove after feedview is working correctly
    missing_outdir = os.path.join(output, 'feedback__view_pages')
    os.makedirs(missing_outdir, exist_ok=True)
    run(f'{FEEDBACK} --view', inpath, output)


RUNNER = [
    'decider_border',
    'decider_textflow',
    'feedback',
    'feedback_decider_border',
    'groupme',
    'rawmaker',
    'textflow',
]


def check(runner=None):
    if runner is None:
        runner = RUNNER
    # TODO: ADD AFTER UPGRADIG UTILA add --version --verbose
    todo = [f'{process} --version --verbose' for process in runner]
    # TODO USE VERBOSE FLAG ON RUN_PARALLEL
    for item in runner:
        utila.log(f'check: {item}')
    # run in parallel to reduce startup time
    ret = utila.fork(todo, worker=len(RUNNER), process=False)
    if not isinstance(ret, list):
        utila.error('runs with error')
        exit(ret)
    utila.log()  # add newline


def assert_validdocument(document: str):
    """Accepted chars are character, numbers and underscore."""
    valid = [item.isalnum() or item == '_' for item in document]
    assert all(valid), str(document)  # ensure to pass no path
