# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila

import queuemo.recipes
from queuemo.recipes import decider_toc
from queuemo.recipes import groupme
from queuemo.recipes import rawmaker


def run(workspace: str, document):
    """Run validation to check that """
    resource = os.path.join(workspace, document)
    assert os.path.exists(resource), str(resource)

    extract_resource(workspace, document)

    tableofcontent(workspace)

    publish(workspace, document)

    close(document)


def resultpath(document: str):
    result = os.path.join(configo.todo(True), document, 'result')
    return result


RESULTVIEW_TOC = 'result/toc'


def extract_resource(workspace: str, document: str):
    queuemo.recipes.assert_validdocument(document)

    outpath = os.path.join(workspace, RESULTVIEW_TOC)
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
        pages='0:5',
    )
    assert completed == 0, str(completed)


def tableofcontent(workspace: str):
    groupme(workspace, 'result/toc', 'result/toc')
    decider_toc(workspace, 'result/toc', 'result/toc')


def publish(workspace: str, document: str):
    queuemo.recipes.assert_validdocument(document)

    publish_fast(workspace, document, 'toc')


def publish_fast(workspace, document, source):

    os.makedirs(resultpath(document), exist_ok=True)

    sourcepath = os.path.join(workspace, 'result')
    sourcepath = os.path.join(sourcepath, source)

    utila.copy_content(sourcepath, resultpath(document), pattern='*_user.yaml')


def close(document: str):
    """Create a file named close to signal update hander that process is
    completed."""
    queuemo.recipes.assert_validdocument(document)
    donepath = os.path.join(resultpath(document), 'done')
    # TODO: ADD STATUS INFORMATION LATER
    utila.file_create(donepath)
