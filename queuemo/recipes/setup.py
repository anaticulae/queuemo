# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import exists
from os.path import join
from shutil import copy

from utila import call
from utila import copy_content
from utila import debug

from queuemo import ROOT


def before(workspace: str):
    # TODO: move logging to global
    call('before setup')
    # TODO: add environment check


def run(workspace: str, document: int):
    assert exists(workspace), workspace
    for item in [
            'config',
            'raw',
            'result',
    ]:
        path = join(workspace, item)
        debug('create dir: %s' % path)
        makedirs(path, exist_ok=True)

    # copy config to workspace
    sourceconfig = join(ROOT, 'config')
    destconfig = join(workspace, 'config')
    copy_content(sourceconfig, destconfig)

    # extract pdf file
    sourcepdf = join(workspace, document)
    assert exists(sourceconfig)
    destpdf = join(workspace, 'work.pdf')
    copy(sourcepdf, destpdf)
