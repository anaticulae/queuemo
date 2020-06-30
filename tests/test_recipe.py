# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import queuemo.runtime
import queuemo.worker.startup
import tests
import tests.resources


@utilatest.skip_nightly
def test_recipe_run(testdir, monkeypatch):
    root = str(testdir)
    with tests.patch_todo(testdir, monkeypatch):
        workspace = queuemo.worker.startup.copy(tests.resources.EXAMPLE_JOB)
        result = queuemo.runtime.run(
            workspace,
            tests.resources.EXAMPLE_JOB,
            root,
        )
    assert result, result
