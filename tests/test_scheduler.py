# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo.directory
import utilatest

import queuemo.runtime.api
import queuemo.worker.startup
import tests


@utilatest.nightly
def test_run_steps(capsys, td, mp):
    config = queuemo.runtime.api.RecipeConfig()
    with tests.patch_todo(td, mp):
        queuemo.worker.startup.step(job=None, config=config)
        assert 'Wait' in utilatest.stdout(capsys)
        queuemo.worker.startup.step(job='8166109011', config=config)
        progress = utilatest.stdout(capsys)
        assert 'Copy' in progress
        assert 'Start' in progress
        assert 'Finish' in progress


def test_copy_job_to_workspace(td, mp):
    with mp.context() as context:
        context.setattr(
            os,
            'environ',
            {
                configo.directory.TODO: tests.resources.TODO,
                configo.directory.TMP: td.tmpdir,
            },
        )
        workspace = queuemo.worker.startup.copy(tests.resources.EXAMPLE_JOB)
        assert os.path.exists(workspace), workspace
