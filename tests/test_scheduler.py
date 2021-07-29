# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo.directory
import utilatest

import queuemo.worker.startup
import tests


@utilatest.nightly
def test_run_steps(capsys, testdir, monkeypatch):
    with tests.patch_todo(testdir, monkeypatch):
        queuemo.worker.startup.step(None)
        assert 'Wait' in utilatest.stdout(capsys)
        queuemo.worker.startup.step('8166109011')
        progress = utilatest.stdout(capsys)
        assert 'Copy' in progress
        assert 'Start' in progress
        assert 'Finish' in progress


def test_copy_job_to_workspace(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(
            os,
            'environ',
            {configo.directory.TODO: tests.resources.TODO},
        )
        workspace = queuemo.worker.startup.copy(tests.resources.EXAMPLE_JOB)
        assert os.path.exists(workspace), workspace
