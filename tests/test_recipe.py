# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import queuemo.recipe
import queuemo.worker.scheduler
import tests
import tests.resources


@utila.skip_longrun
def test_recipe_run(testdir, monkeypatch):
    root = str(testdir)
    with tests.patch_todo(testdir, monkeypatch):
        workspace = queuemo.worker.scheduler.copy(tests.resources.EXAMPLE_JOB)
        result = queuemo.recipe.run(
            workspace,
            tests.resources.EXAMPLE_JOB,
            root,
        )
    assert result, result
