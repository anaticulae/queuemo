# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilotest

import queuemo.runtime.api
import queuemo.worker.startup
import tests
import tests.conftest
import tests.resources


@utilotest.nightly
def test_run_steps(capsys, td, mp):
    config = queuemo.runtime.api.RecipeConfig()
    with tests.patch_todo(td, mp):
        queuemo.worker.startup.step(job=None, config=config)
        assert '.' in utilotest.stdout(capsys)
        queuemo.worker.startup.step(
            job=tests.resources.EXAMPLE_JOB,
            config=config,
        )
        progress = utilotest.stdout(capsys)
        assert 'Copy' in progress
        assert 'Start' in progress
        assert 'Finish' in progress


@tests.conftest.generated
def test_copy_job_to_workspace(td, mp):
    with tests.patch_todo(td, mp):
        workspace = queuemo.worker.startup.copy(tests.resources.EXAMPLE_JOB)
        assert os.path.exists(workspace), workspace
