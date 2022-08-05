# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utila

import queuemo.runnable
import queuemo.runtime.api


def determine_sections(flow: queuemo.runtime.api.RecipeIO, pages=':'):
    # PAGES is required to avoid running sections --paper on the whole
    # document. This is not required for running fastview on first 20
    # pages.
    pagenumber_footnotes_headnotes(flow, pages)
    queuemo.runnable.groupme(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        footer=True,
        pages=pages,
    )
    # required for sections --docinfo
    utila.file_copy(link.pdfinfo_path(flow.document), flow.tmppath)
    # determine to run area of feature detection
    queuemo.runnable.sections(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        pdf=flow.sourcepath,
        pages=pages,
    )


def pagenumber_footnotes_headnotes(
    flow: queuemo.runtime.api.RecipeIO,
    pages: str,
):
    queuemo.runnable.pagenumber(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        pages=pages,
    )
    queuemo.runnable.cleanup_cleanup(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        select='pagenumber',
    )
    queuemo.runnable.footnote(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        pages=pages,
    )
    queuemo.runnable.cleanup_cleanup(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        select='footnote',
    )
    queuemo.runnable.headnote(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        pages=pages,
    )
    queuemo.runnable.cleanup_cleanup(
        inpath=flow.tmppath,
        outpath=flow.tmppath,
        select='headnote',
    )
