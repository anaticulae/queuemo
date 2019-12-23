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

import utila
from pytest import fixture

import queuemo.recipes.setup as setup
from queuemo.recipe import run as run_recipe
from queuemo.recipes import COMMON_VIEW_WORK
from queuemo.recipes.analysis import before as analysis_before
from queuemo.recipes.commonview import after as commonview_after
from queuemo.recipes.commonview import before as commonview_before
from queuemo.recipes.commonview import run as commonview_run
from queuemo.recipes.docsplit import before as docsplit_before
from queuemo.recipes.docsplit import run as docsplit_run
from queuemo.recipes.docsplit import workingpath as docsplit_workingpath
from queuemo.recipes.extractraw import OUTPATH as RAWMAKER_OUTPATH
from queuemo.recipes.extractraw import run as run_extractraw
from queuemo.worker.scheduler import copy
from tests import EXAMPLE_JOB
from tests import EXAMPLE_PDF
from tests import patch_todo


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
    return rawspace, expected_result


@fixture
def docsplit_result(rawmaker_result):  # pylint:disable=W0621
    """Run rawmaker twice and extract sections"""
    rawspace, _ = rawmaker_result  # pylint:disable=W0621
    docsplit_before(rawspace)
    docsplit_run(rawspace)

    return rawspace, docsplit_workingpath(rawspace)


@utila.skip_longrun
def test_recipe_run(testdir, monkeypatch):
    with patch_todo(testdir, monkeypatch):
        workspace = copy(EXAMPLE_JOB)
        result = run_recipe(workspace, EXAMPLE_JOB)
    assert result, result


def test_recipe_workspace_setup(rawspace):  # pylint:disable=W0621
    rawspacepath = rawspace
    assert exists(rawspacepath)


@utila.skip_longrun
def test_recipe_extractraw_run(rawmaker_result):
    result = listdir(rawmaker_result[1])

    # this value may change in the future, but it is not so important. Existing
    # files signals working feature.
    circa_eight = 8
    assert len(result) > circa_eight, str(result)


@utila.skip_longrun
def test_recipe_docsplit_run(docsplit_result):  # pylint:disable=W0621
    _, docsplitpath = docsplit_result
    result = listdir(docsplitpath)
    circa_fifteen = 15
    assert len(result) >= circa_fifteen, str(result)


@utila.skip_longrun
def test_recipe_commonview_run(docsplit_result):  # pylint:disable=W0621
    rawspace_, _ = docsplit_result

    analysis_before(rawspace_)

    commonview_before(rawspace_)
    commonview_run(rawspace_)
    commonview_after(rawspace_)

    workingpath = join(rawspace_, COMMON_VIEW_WORK)
    result = listdir(workingpath)

    assert len(result) > 20, str(result)
