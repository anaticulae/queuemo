# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os
from os.path import exists

from configo.share import TODO as SHARED_TODO

from queuemo.worker.scheduler import copy
from queuemo.worker.scheduler import step
from tests import EXAMPLE_JOB
from tests import TODO
from tests import patch_todo


def content(capture):
    return capture.readouterr().out


def test_run(capsys, tmpdir, monkeypatch):
    step(None)
    assert 'Wait' in content(capsys)

    with patch_todo(tmpdir, monkeypatch):
        step('8166109011')
        progress = content(capsys)
        assert 'Copy' in progress
        assert 'Start' in progress
        assert 'Finish' in progress


def test_copy_job_to_workspace(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(os, 'environ', {SHARED_TODO: TODO})

        temp_workspace = copy(EXAMPLE_JOB)
        assert exists(temp_workspace), temp_workspace
