# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from queuemo.receipe import run
from queuemo.worker.scheduler import copy
from tests import EXAMPLE_JOB
from tests import patch_todo


def test_run_receipe(tmpdir, monkeypatch):
    with patch_todo(tmpdir, monkeypatch):
        workspace = copy(EXAMPLE_JOB)

        result = run(workspace, EXAMPLE_JOB)
    assert result, result
