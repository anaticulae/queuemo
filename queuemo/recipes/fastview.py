# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila

import queuemo.recipes
from queuemo.recipes import decider_titlepage
from queuemo.recipes import detector
from queuemo.recipes import rawmaker


def run(workspace: str, document):
    queuemo.recipes.assert_validdocument(document)
    resource = os.path.join(workspace, document)
    assert os.path.exists(resource), str(resource)

    extract_resource(workspace, document)

    # jobs
    titlepage(workspace, document)

    # use public to push results after every finished job
    publish(workspace, document)

    close(document)


FASTVIEW_TITLEPAGE = 'fastview/titlepage'


def extract_resource(workspace: str, document: str):
    queuemo.recipes.assert_validdocument(document)

    outpath = os.path.join(workspace, FASTVIEW_TITLEPAGE)
    os.makedirs(outpath, exist_ok=True)

    resource = os.path.join(workspace, document)
    assert os.path.exists(resource), str(resource)
    # TODO: REMOVE AFTER UPGRADING RAWMAKER WHICH SUPPORTS FILES AS INPUT
    source = os.path.join(outpath, 'work.pdf')
    utila.file_copy(resource, source)

    completed = rawmaker(
        workspace,
        inpath=source,
        outpath=outpath,
        prefix='oneline',
        pages='0',
    )
    assert completed == 0, str(completed)


def titlepage(workspace: str, document: str):
    queuemo.recipes.assert_validdocument(document)
    detector(workspace, FASTVIEW_TITLEPAGE, FASTVIEW_TITLEPAGE)
    decider_titlepage(workspace, FASTVIEW_TITLEPAGE, FASTVIEW_TITLEPAGE)


def publish(workspace: str, document: str):
    queuemo.recipes.assert_validdocument(document)

    publish_fast(workspace, document, 'titlepage', 1)


def publish_fast(workspace, document, source, destination: int):
    sourcepath = os.path.join(workspace, 'fastview')
    sourcepath = os.path.join(sourcepath, source)

    fastpath = os.path.join(configo.todo(True), document, 'fastview')
    destination = str(destination).zfill(2)
    destination = os.path.join(fastpath, f'{destination}_{source}')

    utila.copy_content(sourcepath, destination, pattern='*_user.yaml')


def close(document: str):
    """Create a file named close to signal update hander that process is
    completed."""
    queuemo.recipes.assert_validdocument(document)
    fastpath = os.path.join(configo.todo(True), document, 'fastview')
    donepath = os.path.join(fastpath, 'done')
    # TODO: ADD STATUS INFORMATION LATER
    utila.file_create(donepath)
