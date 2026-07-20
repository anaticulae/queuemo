# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import hoverpower
import pytest
import utilo
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import queuemo
import queuemo.cli.utils
import tests.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(queuemo.ROOT)
PACKAGE = queuemo.PROCESS

RESOURCES_TODO = [
    hoverpower.BACHELOR085_PDF,
    hoverpower.HOME025_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER078_PDF,
    hoverpower.MASTER083_PDF,
    hoverpower.MASTER089_PDF,
    hoverpower.MASTER116_PDF,
    hoverpower.ORDER009_PDF,
    hoverpower.ORDER038_PDF,
    hoverpower.PAPER06_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    os.makedirs(configos.todo(), exist_ok=True)
    os.makedirs(configos.ready(), exist_ok=True)
    hoverpower.run()
    # TODO: HACK BUT WORKS FOR THE MOMENT
    queuemo.cli.utils.logger_start()


def extract_todo(files):
    tests.update.extract_examples(files)


GENERATED = utilo.exists(os.path.join(hoverpower.generated(), 'todo'))
generated = pytest.mark.skipif(not GENERATED, reason='generate test test')
