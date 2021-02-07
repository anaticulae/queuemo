# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Runner overview
===============
"""

import os

import rawmaker.cli as rawmaker_cli
import utila

TIMEOUT_DEFAULT = 60 * 10  # ten minutes per step


def run(
        runnable: str,
        inpath: utila.Strings,
        outpath: str,
        parameter: str = None,
        prefix: str = '',
        timeout=None,
        **kwargs,
) -> int:
    inpath, outpath, prefix = prepare_run(inpath, outpath, prefix)
    cmds = kwargs_to_parameter(kwargs)

    parameter = ' ' if parameter is None else parameter
    cmd = f'{runnable} {parameter} -i {inpath} -o {outpath} {prefix} {cmds}'

    if timeout is None or isinstance(timeout, (float, int)):
        timeout = utila.Timeout(
            seconds=timeout if timeout is not None else TIMEOUT_DEFAULT,
            gracefully=False,
        )
    utila.log(f'>> {cmd} <<')
    utila.debug(f'timeout: {timeout.seconds}')
    with utila.profile(runnable):
        completed = utila.run(cmd, timeout=timeout)

    utila.log(completed.stdout)
    assert os.path.exists(outpath), str(outpath)
    return completed


def prepare_run(inpath, outpath, prefix):
    if isinstance(inpath, str):
        inpath = [inpath]
    # beautify path: remove ../..
    outpath = os.path.normpath(outpath)
    inpath = [os.path.normpath(item) for item in inpath]
    for item in inpath:
        assert os.path.exists(item), item
    # single inputpath does not produces -i, see str.join docu
    inpath: str = ' -i '.join(inpath)
    prefix = f'--prefix={prefix}' if prefix else ''
    return inpath, outpath, prefix


def kwargs_to_parameter(args: dict) -> str:
    """\
    >>> kwargs_to_parameter(dict(footer=False, pagenumbers=False))
    '--footer! --pagenumbers!'
    """
    if not args:
        return ''
    cmds = []
    for param, value in args.items():
        if value is True:
            cmds.append(f'--{param}')
        elif value is False:
            # TODO: VERIFY LATER
            cmds.append(f'--{param}!')
            continue
        else:
            cmds.append(f'--{param} {value}')
    result = ' '.join(cmds)
    return result


CHAR_MARGIN_DEFAULT = float(rawmaker_cli.CHAR_MARGIN.defaultvar)
BOXES_FLOW_DEFAULT = float(rawmaker_cli.BOXES_FLOW.defaultvar)


def rawmaker(
        inpath: str,
        outpath: str = None,
        process: int = 8,
        prefix: str = '',
        char_margin: float = CHAR_MARGIN_DEFAULT,
        boxes_flow: float = BOXES_FLOW_DEFAULT,
        **kwargs,
) -> int:
    """Run external rawmaker.

    Args:
        inpath(str): relative input path
        outpath(str): relative output path
        process(int): use amount of parallel runner
        prefix(str): to extend the output name with a prefix
        char_margin(float): maximal distance between two chars
        boxes_flow(float): ratio betwee horizontal and vertical analysis
        kwargs(dict): ???
    Returns:
        0 if process succeeded else failure code
    """
    if isinstance(inpath, str):
        inpath = [inpath]
    kwargs[rawmaker_cli.CHAR_MARGIN.name] = char_margin
    kwargs[rawmaker_cli.BOXES_FLOW.name] = boxes_flow
    returncode = run(
        'rawmaker',
        inpath,
        outpath,
        f'-j={process}',
        prefix,
        **kwargs,
    )
    return returncode


def linero(inpath: str, output: str = None, timeout: int = None, **kwargs):
    return run('linero', inpath, output, timeout=timeout, **kwargs)


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
    run('decider_footnote -j8', inpath, output)


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
    run('textflow --quotation --blockquote -j2', inpath, output, **kwargs)


def doctextstyle(inpath: str, output: str = None, **kwargs):
    run('doctextstyle', inpath, output, **kwargs)


def caption(inpath: str, output: str = None, **kwargs):
    run('caption -j8', inpath, output, **kwargs)


def magic(inpath: str, output: str = None, **kwargs):
    run('magic', inpath, output, **kwargs)


def docref(inpath: str, output: str = None, **kwargs):
    run('docref -j4', inpath, output, **kwargs)


def docref_bibliography(inpath: str, output: str = None, **kwargs):
    run('docref --bibliography', inpath, output, **kwargs)


def chapter(inpath: str, output: str = None, **kwargs):
    run('chapter', inpath, output, **kwargs)


def smarty(inpath: str, output: str = None, **kwargs):
    run('smarty', inpath, output, **kwargs)


def decider_abbreviation(inpath: str, output: str = None, **kwargs):
    run('decider_abbreviation', inpath, output, **kwargs)


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
    run('decider_textflow -j8', inpath, output, **kwargs)


def feedback_images(inpath: str, output: str = None):
    # TODO: Remove after feedview is working correctly
    missing_outdir = os.path.join(output, 'feedback__view_pages')
    os.makedirs(missing_outdir, exist_ok=True)
    run(f'feedback --images --figures -j2', inpath, output)


def feedback_view(inpath: str, output: str = None):
    # TODO: Remove after feedview is working correctly
    missing_outdir = os.path.join(output, 'feedback__view_pages')
    os.makedirs(missing_outdir, exist_ok=True)
    run(f'feedback --view', inpath, output)


def feedback_plot(inpath: str, output: str = None):
    run(f'feedback --plot', inpath, output)


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
