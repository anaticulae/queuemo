# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import queuemo.recipes.resultview
import tests
import tests.resources
from tests.fixtures.todo import example_8166  # pylint:disable=W0611


@utila.skip_longrun
def test_recipe_resultview_run(example_8166, monkeypatch):  # pylint:disable=W0621
    workspace = str(example_8166)

    todopath = os.path.join(workspace, '_todo')
    with tests.patch_todo(todopath, monkeypatch):
        queuemo.recipes.resultview.run(workspace, tests.resources.EXAMPLE_JOB)
