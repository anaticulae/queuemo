# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import pytest
import utila

import queuemo.recipes.resultview
import tests
import tests.resources
from tests.fixtures.todo import copy_todo
from tests.fixtures.todo import example_8166  # pylint:disable=W0611


@pytest.mark.xfail(reason='re work scheduler')
@utila.skip_longrun
def test_recipe_resultview_run(example_8166, monkeypatch):  # pylint:disable=W0621
    workspace = str(example_8166)

    todopath = os.path.join(workspace, '_todo')
    with tests.patch_todo(todopath, monkeypatch):
        queuemo.recipes.resultview.run(workspace, tests.resources.EXAMPLE_JOB)


@utila.skip_longrun
@pytest.mark.xfail(reason='re work scheduler')
@pytest.mark.parametrize('jobid', [
    '2324123123',
    'howtowrite_pages9',
    'page_116_images_toc_formular',
    'page_38',
    'page_72_noimages_toc',
    'page_78_images_toc',
    'page_83_noimages_toc',
    'page_89_noimages_toc',
])
def test_recipe_resultview_run_example(jobid, testdir, monkeypatch):  # pylint:disable=W0621
    workspace = str(testdir)
    copy_todo(jobid, workspace)

    todopath = os.path.join(workspace, '_todo')
    with tests.patch_todo(todopath, monkeypatch):
        queuemo.recipes.resultview.run(workspace, jobid)
