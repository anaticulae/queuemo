# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import tests.resources


@pytest.fixture
def example_8166(testdir):
    root = str(testdir)
    source = os.path.join(
        tests.resources.TODO,
        tests.resources.EXAMPLE_JOB,
        tests.resources.EXAMPLE_JOB,
    )
    destination = os.path.join(
        root,
        tests.resources.EXAMPLE_JOB,
    )
    utila.file_copy(source, destination)
    return root
