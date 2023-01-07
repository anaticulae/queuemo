# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import power
import pytest
import utila
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import queuemo
import queuemo.cli.utils
import tests.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(queuemo.ROOT)
PACKAGE = queuemo.PROCESS

RESOURCES_TODO = [
    power.BACHELOR085_PDF,
    power.HOME025_PDF,
    power.MASTER072_PDF,
    power.MASTER078_PDF,
    power.MASTER083_PDF,
    power.MASTER089_PDF,
    power.MASTER116_PDF,
    power.ORDER009_PDF,
    power.ORDER038_PDF,
    power.PAPER06_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    os.makedirs(configo.todo(), exist_ok=True)
    os.makedirs(configo.ready(), exist_ok=True)
    power.run()
    # TODO: HACK BUT WORKS FOR THE MOMENT
    queuemo.cli.utils.logger_start()


def extract_todo(files):
    tests.update.extract_examples(files)


GENERATED = utila.exists(os.path.join(power.generated(), 'todo'))
generated = pytest.mark.skipif(not GENERATED, reason='generate test test')
