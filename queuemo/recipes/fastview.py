# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import time

import configo
import utila

from queuemo.recipes import decider_decider
from queuemo.recipes import decider_titlepage
from queuemo.recipes import detector
from queuemo.recipes import groupme
from queuemo.recipes import rawmaker


def extract_resource(workspace: str, document: str):
    assert document.isalnum(), str(document)  # ensure to pass no path
    outpath = os.path.join(workspace, 'fastview/titlepage')
    os.makedirs(outpath, exist_ok=True)
    resource = os.path.join(workspace, document)
    assert os.path.exists(resource), str(resource)
    # TODO: REMOVE AFTER UPGRADING RAWMAKER WHICH SUPPORTS FILES AS INPUT
    destination = os.path.join(outpath, 'work.pdf')
    utila.file_copy(resource, destination)

    completed = rawmaker(
        workspace,
        inpath=destination,
        outpath=outpath,
        prefix='oneline',
        pages='0',
    )
    assert completed == 0, str(completed)


def titlepage(workspace: str, document: str):
    detector(workspace, 'fastview/titlepage', 'fastview/titlepage')
    decider_titlepage(workspace, 'fastview/titlepage', 'fastview/titlepage')
