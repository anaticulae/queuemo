# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Runner overview
===============
"""

import functools
import os
import sys

import rawmaker.cli as rawmaker_cli
import utila

# TODO: DECREASE BEFORE GOING LIVE!
TIMEOUT_DEFAULT = 60 * 10 * 2  # twenty minutes per step


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
    cmd = utila.normalize_whitespaces(cmd)

    if timeout is None or isinstance(timeout, (float, int)):
        timeout = utila.Timeout(
            seconds=timeout if timeout is not None else TIMEOUT_DEFAULT,
            gracefully=False,
        )
    utila.log(f'>>{cmd}<<')
    utila.debug(f'timeout: {timeout.seconds}')
    with utila.profile(runnable, always=True):
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
    >>> kwargs_to_parameter(dict(table='C:/file/pdf.pdf'))
    '--table C:/file/pdf.pdf'
    """
    if not args:
        return ''
    cmds = []
    for param, value in args.items():
        if value is True:
            cmds.append(f'--{param}')
        elif value is False:  # pylint:disable=C2001
            # TODO: VERIFY LATER
            cmds.append(f'--{param}!')
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
        outpath(str): relative outpath path
        process(int): use amount of parallel runner
        prefix(str): to extend the outpath name with a prefix
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


def tablero(inpath: str, outpath: str = None, timeout: int = None, **kwargs):
    return run('tablero', inpath, outpath, timeout=timeout, **kwargs)


def formulero(inpath: str, outpath: str = None, timeout: int = None, **kwargs):
    return run('formulero', inpath, outpath, timeout=timeout, **kwargs)


def spacestation(inpath: str, outpath: str = None, **kwargs):  # pylint:disable=W0613
    utila.error('TODO: ENABLE SPACESTATION BEFORE RELEASE')
    # run('spacestation', inpath, outpath, **kwargs)


def groupme(inpath: str, outpath: str = None, **kwargs):
    run('groupme -j8', inpath, outpath, **kwargs)


def reftable(inpath: str, outpath: str = None, **kwargs):
    run('reftable -j4', inpath, outpath, **kwargs)


def codero(inpath: str, outpath: str = None, **kwargs):
    run('codero', inpath, outpath, **kwargs)


def cleanup(inpath: str, outpath: str = None, **kwargs):
    return run('cleanup', inpath, outpath, **kwargs)


def figureo(inpath: str, outpath: str = None, **kwargs):
    return run('figureo', inpath, outpath, **kwargs)


def sections(inpath: str, outpath: str = None, **kwargs):
    run('sections -j8', inpath, outpath, **kwargs)


def headlines(inpath: str, outpath: str = None, **kwargs):
    run('headlines -j4', inpath, outpath, **kwargs)


def words(inpath: str, outpath: str = None, **kwargs):
    run('words -j8', inpath, outpath, **kwargs)


def words_links(inpath: str, outpath: str = None, **kwargs):
    run('words --links', inpath, outpath, **kwargs)


def lists(inpath: str, outpath: str = None, **kwargs):
    run('lists', inpath, outpath, **kwargs)


def detector_formula(inpath: str, outpath: str, **kwargs):
    run('detector --formula', inpath, outpath, **kwargs)


def detector_titlepage(inpath: str, outpath: str = None, **kwargs):
    run('detector --titlepage', inpath, outpath, **kwargs)


def detector_index(inpath: str, outpath: str = None, **kwargs):
    run('detector --index', inpath, outpath, **kwargs)


def colors_statistics(inpath: str, outpath: str = None, **kwargs):
    run('colors --statistics', inpath, outpath, **kwargs)


def decider_titlepage(inpath: str, outpath: str = None):
    run('decider --titlepage', inpath, outpath)


def decider_toc(inpath: str, outpath: str = None):
    run('decider_toc', inpath, outpath)


def decider_footnote(inpath: str, outpath: str = None):
    run('decider_footnote -j8', inpath, outpath)


def decider_imgfig(inpath: str, outpath: str = None, **kwargs):
    run('decider_imgfig', inpath, outpath, **kwargs)


def decider_border_detecion(inpath: str, outpath: str = None):
    run('decider_border --detection', inpath, outpath)


def decider_border_distance(inpath: str, outpath: str = None):
    run('decider_border --distance', inpath, outpath)


def decider_color(inpath: str, outpath: str = None):
    run('decider --color', inpath, outpath)


def textflow_alignment(inpath: str, outpath: str = None, **kwargs):
    run('textflow --alignment', inpath, outpath, **kwargs)


def textflow_lineending(inpath: str, outpath: str = None, **kwargs):
    run('textflow --lineending', inpath, outpath, **kwargs)


def textflow_wordspace(inpath: str, outpath: str = None, **kwargs):
    run('textflow --wordspace', inpath, outpath, **kwargs)


def textflow_quotes(inpath: str, outpath: str = None, **kwargs):
    run('textflow --quotation --blockquote -j2', inpath, outpath, **kwargs)


def doctextstyle(inpath: str, outpath: str = None, **kwargs):
    run('doctextstyle', inpath, outpath, **kwargs)


def caption(inpath: str, outpath: str = None, **kwargs):
    run('caption -j8', inpath, outpath, **kwargs)


def magic(inpath: str, outpath: str = None, **kwargs):
    run('magic', inpath, outpath, **kwargs)


def docref(inpath: str, outpath: str = None, **kwargs):
    run('docref -j4', inpath, outpath, **kwargs)


def docref_bibliography(inpath: str, outpath: str = None, **kwargs):
    run('docref --bibliography', inpath, outpath, **kwargs)


def chapter(inpath: str, outpath: str = None, **kwargs):
    run('chapter', inpath, outpath, **kwargs)


def smarty(inpath: str, outpath: str = None, **kwargs):
    run('smarty', inpath, outpath, **kwargs)


def decider_abbreviation(inpath: str, outpath: str = None, **kwargs):
    run('decider_abbreviation', inpath, outpath, **kwargs)


def decider_smarty(inpath: str, outpath: str = None, **kwargs):
    run('decider_smarty', inpath, outpath, **kwargs)


def decider_bibliography(inpath: str, outpath: str = None, **kwargs):
    run('decider_bibliography', inpath, outpath, **kwargs)


def decider_chapter(inpath: str, outpath: str = None, **kwargs):
    run('decider_chapter', inpath, outpath, **kwargs)


def decider_textstyle_headlines(inpath: str, outpath: str = None, **kwargs):
    # TODO: Enable later; activate after utila supports selective inputs
    # run('decider_textflow --lineending', inpath, outpath)
    run('decider_textstyle --headlines', inpath, outpath, **kwargs)


def decider_textstyle_text(inpath: str, outpath: str = None, **kwargs):
    run('decider_textstyle --text', inpath, outpath, **kwargs)


def bibliography(inpath: str, outpath: str = None, **kwargs):
    run('bibliography', inpath, outpath, **kwargs)


def decider_links(inpath: str, outpath: str = None):
    run('decider --links', inpath, outpath)


def decider_textflow_lineending(inpath: str, outpath: str = None, **kwargs):
    # TODO: Enable later; activate after utila supports selective inputs
    # run('decider_textflow --lineending', inpath, outpath)
    run('decider_textflow -j8', inpath, outpath, **kwargs)


def feedback_images(inpath: str, outpath: str = None):
    # TODO: Remove after feedview is working correctly
    missing_outdir = os.path.join(outpath, 'feedback__view_pages')
    os.makedirs(missing_outdir, exist_ok=True)
    run('feedback --images --figures -j2', inpath, outpath)


def feedback_view(inpath: str, outpath: str = None):
    # TODO: Remove after feedview is working correctly
    missing_outdir = os.path.join(outpath, 'feedback__view_pages')
    os.makedirs(missing_outdir, exist_ok=True)
    run('feedback --view', inpath, outpath)


def feedback_plot(inpath: str, outpath: str = None):
    run('feedback --plot', inpath, outpath)


def feedback_findings(inpath: str, pdf: str, outpath: str = None):
    run(f'feedback --findings --pdf {pdf}', inpath, outpath)


def ghost(inpath: str, outpath: str = None):
    run('ghost', inpath, outpath)


# TODO: USE RUNTIME.py AS SOURCE/METHODS FOR AVAILABLE RUNNER
RUNNER = utila.splitlines("""
caption
chapter
cleanup
codero
decider
decider_abbreviation
decider_bibliography
decider_border
decider_chapter
decider_footnote
decider_imgfig
decider_smarty
decider_textflow
decider_textstyle
decider_toc
detector
docref
doctextstyle
feedback
figureo
ghost
groupme
headlines
magic
queuemo
rawmaker
reftable
sections
smarty
spacestation
tablero
textflow
words
""")


def check(runner=None):
    if runner is None:
        runner = RUNNER
    todo = [
        functools.partial(utila.run, f'{process} -v -VVV')
        for process in sorted(runner)
    ]
    for item in runner:
        utila.debug(f'check: {item}')
    # run in parallel to reduce startup time
    ret = utila.fork(*todo, worker=len(RUNNER), process=False)
    if not isinstance(ret, list):
        utila.error('runs with error')
        sys.exit(ret)
    for item in ret:
        if item.returncode:
            utila.error(item)
            continue
        utila.log(item.stdout.strip())
    utila.log()  # add newline


def assert_validdocument(document: str):
    """Accepted chars are character, numbers and underscore."""
    valid = [item.isalnum() or item == '_' for item in document]
    assert all(valid), str(document)  # ensure to pass no path
