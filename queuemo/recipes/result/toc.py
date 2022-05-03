# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Toc
===
"""

import os

import iamraw.sections
import serializeraw
import utila

import queuemo.runnable
import queuemo.runtime.api


def run(flow: queuemo.runtime.api.RecipeIO):
    pages = queuemo.utils.select_pages(
        flow.general,
        select=iamraw.sections.TableOfContent,
    )
    if pages == ':':
        utila.log('could not detect TableOfContent page-numbers')
        create_backup_toc(flow.general)
        return
    queuemo.runnable.reftable(
        inpath=[flow.general],
        outpath=flow.general,
        toc=True,
        pages=pages,
    )


def create_backup_toc(outpath: str):
    outpath = os.path.join(outpath, 'reftable__toc_toc.yaml')
    utila.log(f'write empty toc: {outpath}')
    dumped = serializeraw.dump_toc(iamraw.Toc())
    utila.file_create(outpath, dumped)
