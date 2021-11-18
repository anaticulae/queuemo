# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw.sections
import link
import serializeraw
import utila

import queuemo
import queuemo.recipes.utils
import queuemo.runnable
import queuemo.runtime.api

TIMEOUT_RESULT_TABLERO = configo.HV_INT_PLUS(default=120)


@queuemo.required
def before(flow: queuemo.runtime.api.RecipeIO):
    if link.current(flow.document) == link.ProcessState.VERIFIED:
        # if fastview is not started before, start analysis with resultview
        link.start_analysis(flow.document)


@queuemo.required
def run(flow: queuemo.runtime.api.RecipeIO):
    unpack_pdf(flow)
    queuemo.recipes.utils.determine_sections(flow)
    publish_pagenumbers(flow)

    queuemo.runnable.groupme(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        # pagenumbers=True, already done by determine_sections
        # footer=True,
        content=True,
    )


def run_code_tab_form_figure(flow: queuemo.runtime.api.RecipeIO):
    timeout = utila.Timeout(
        seconds=TIMEOUT_RESULT_TABLERO,
        gracefully=True,
    )
    valid_pages = valid_figures_tables(flow)
    # ensure rawmaker is completed before running tablero
    queuemo.runnable.codero(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        pages=valid_pages,
    )
    queuemo.runnable.tablero(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        table=flow.sourcepath,
        timeout=timeout,
        pages=valid_pages,
    )
    pdf = flow.sourcepath
    queuemo.runnable.formulero(
        inpath=pdf,
        outpath=flow.tmppath,
        timeout=timeout,
        pages=valid_pages,
    )
    queuemo.runnable.figureo(
        inpath=[
            pdf,
            flow.tmppath,
        ],
        outpath=flow.tmppath,
        pages=valid_pages,
        standard=True,
    )
    queuemo.runnable.figureo(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        pages=valid_pages,
        cleanup=True,
    )


def run_cleanup(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.rawmaker_cleanup(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
    )
    queuemo.runnable.rawmaker_cleanup(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        prefix='oneline',
    )


def run_final(flow: queuemo.runtime.api.RecipeIO):
    queuemo.runnable.groupme(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        toc=False,
        footer=False,
        pagenumbers=False,
        abbreviation=False,
        content=False,
    )


def unpack_pdf(flow: queuemo.runtime.api.RecipeIO):
    pdf = flow.sourcepath
    with utila.GeorgFork(worker=2, process=False) as runtime:
        # use 2 worker to start spacestation after finishing first rawmaker
        runtime.fork(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            all=True,
        )
        runtime.fork(
            queuemo.runnable.rawmaker,
            inpath=pdf,
            outpath=flow.tmppath,
            prefix='oneline',
            boxes_flow=1.0,
            char_margin=100,
            line_margin=0.1,
            text=True,
            fonts=True,
            process=1,
        )
        runtime.fork(
            queuemo.runnable.spacestation,
            inpath=pdf,
            outpath=flow.tmppath,
        )
    assert runtime.result == utila.SUCCESS, 'could not extract pdf'


NO_FIGURE_TABLES = (
    iamraw.sections.Acknowledgments,
    iamraw.sections.Bibliography,
    iamraw.sections.FigureTable,
    iamraw.sections.Glossary,
    iamraw.sections.Index,
    iamraw.sections.SymbolTable,
    iamraw.sections.TableOfContent,
    iamraw.sections.TableTable,
    iamraw.sections.WhitePage,
)


def valid_figures_tables(flow: queuemo.runtime.api.RecipeIO) -> str:
    sections = serializeraw.load_sections(flow.tmppath)
    valid = []
    for part in sections:
        if isinstance(part, iamraw.sections.Introduction):
            continue
        if isinstance(part, iamraw.sections.CiteContent):
            continue
        if isinstance(part, iamraw.sections.MainPart):
            for item in part:
                for page in range(item.start, item.end + 1):
                    valid.append(page)
            continue
        # Appendix or Unknown
        for item in part:
            if isinstance(item, NO_FIGURE_TABLES):
                continue
            for page in range(item.start, item.end + 1):
                valid.append(page)
    result = utila.simplify_pages(valid)
    return result


def publish_pagenumbers(flow):
    """Required to render pdf navigation with real page numbers."""
    resultview = link.resultview(flow.document)
    # TODO: REMOVE LATER?
    utila.copy_content(
        flow.general,
        resultview,
        pattern='groupme__pagenumbers_pagenumbers.yaml',
        verbose=True,
    )
