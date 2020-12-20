# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest

import queuemo
import tests.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = queuemo.PROCESS

power.setup(queuemo.ROOT)

RESOURCES_TODO = [
    power.MASTER072_PDF,
    power.MASTER078_PDF,
    power.MASTER083_PDF,
    power.BACHELOR085_PDF,
    power.MASTER089_PDF,
    power.MASTER116_PDF,
    power.ORDER009_PDF,
    power.ORDER038_PDF,
    power.HOME025_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract_todo(files):
    tests.update.extract_examples(files)
