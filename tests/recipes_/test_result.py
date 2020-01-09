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

import queuemo.recipe
import queuemo.recipes.runner
import tests
import tests.resources
from tests.fixtures.todo import runtime


def run_resultview(workspace, jobid, monkeypatch):
    outpath = os.path.join(workspace, 'outpath')
    with runtime(
            workspace,
            jobid,
            recipes=[
                queuemo.recipe.VALIDATION,
                queuemo.recipe.RESULT,
            ],
            monkeypatch=monkeypatch,
            outpath=outpath,
    ) as rt:  # pylint:disable=C0103
        completed = rt.finish()
    return completed


@utila.skip_longrun
def test_recipe_result_run_single(testdir, monkeypatch):  # pylint:disable=W0621
    workspace = str(testdir)
    completed = run_resultview(
        workspace,
        tests.resources.EXAMPLE_JOB,
        monkeypatch,
    )
    assert completed


@utila.skip_longrun
@pytest.mark.parametrize('jobid', [
    '2324123123',
    pytest.param(
        'howtowrite_pages9',
        marks=pytest.mark.xfail(reason='fix bug in groupme'),
    ),
    'page_116_images_toc_formular',
    'page_38',
    'page_72_noimages_toc',
    'page_78_images_toc',
    'page_83_noimages_toc',
    pytest.param(
        'page_89_noimages_toc',
        marks=pytest.mark.xfail(reason='fix bug in groupme'),
    ),
])
def test_recipe_result_run_example(jobid, testdir, monkeypatch):  # pylint:disable=W0621
    workspace = str(testdir)
    completed = run_resultview(
        workspace,
        jobid,
        monkeypatch,
    )
    assert completed
