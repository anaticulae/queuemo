# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import pytest
import utila

import queuemo.recipes.fastview
import tests


@pytest.fixture
def example_8166(testdir):
    root = str(testdir)
    source = os.path.join(tests.TODO, tests.EXAMPLE_JOB, tests.EXAMPLE_JOB)
    destination = os.path.join(root, tests.EXAMPLE_JOB)
    utila.file_copy(source, destination)
    return root


def test_recipe_fastview_extract_resources(example_8166):  # pylint:disable=W0621
    """Ensure that resources for title page analysation is created."""
    workspace = str(example_8166)
    with tests.increased_filecount(workspace):
        queuemo.recipes.fastview.extract_resource(workspace, tests.EXAMPLE_JOB)
