# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir
from os.path import exists
from os.path import join
from shutil import copy as copy_file

from pytest import fixture

import queuemo.recipes.setup as setup
from queuemo.recipe import run
from queuemo.recipes.extractraw import OUTPATH as RAWMAKER_OUTPATH
from queuemo.recipes.extractraw import run as run_extractraw
from queuemo.worker.scheduler import copy
from tests import EXAMPLE_JOB
from tests import EXAMPLE_PDF
from tests import patch_todo

# from utila import copy_content # TODO: REPLACE AFTER UPGRADE


@fixture
def rawspace(testdir) -> str:
    workspace = str(testdir)
    workpdf = join(workspace,)
    rawspacepath = join(workspace, 'raw')
    # TODO: REMOVE AFTER UPGRADE
    copy_file(EXAMPLE_PDF, workspace)
    setup.run(workspace, EXAMPLE_JOB)

    assert exists(workpdf), str(workpdf)
    return rawspacepath


@fixture
def rawmaker_result(rawspace):  # pylint:disable=W0621
    expected_result = join(rawspace, RAWMAKER_OUTPATH)
    run_extractraw(rawspace)
    assert exists(expected_result), str(expected_result)
    return expected_result


def test_recipe_run(testdir, monkeypatch):
    with patch_todo(testdir, monkeypatch):
        workspace = copy(EXAMPLE_JOB)
        result = run(workspace, EXAMPLE_JOB)
    assert result, result


def test_recipe_workspace_setup(rawspace):  # pylint:disable=W0621
    rawspacepath = rawspace
    assert exists(rawspacepath)


def test_recipe_extractraw_run(rawmaker_result):
    result = listdir(rawmaker_result)

    # this value may change in the future, but it is not so important. Existing
    # files signals working feature.
    circa_eight = 8
    assert len(result) > circa_eight, str(result)
