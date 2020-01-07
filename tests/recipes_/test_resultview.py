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


@utila.skip_longrun
def test_recipe_resultview_run_single(testdir):  # pylint:disable=W0621
    workspace = str(testdir)
    tests.fixtures.todo.copy_todo(tests.resources.EXAMPLE_JOB, workspace)
    outpath = os.path.join(workspace, 'outpath')

    runtime = queuemo.recipes.runner.RecipeRuntime(
        workspace=workspace,
        document=tests.resources.EXAMPLE_JOB,
        outpath=outpath,
    )
    runtime.append(queuemo.recipe.RESULT)
    completed = runtime.next_step()
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
def test_recipe_resultview_run_example(jobid, testdir):  # pylint:disable=W0621
    workspace = str(testdir)
    tests.fixtures.todo.copy_todo(jobid, workspace)
    outpath = os.path.join(workspace, 'outpath')

    runtime = queuemo.recipes.runner.RecipeRuntime(
        workspace=workspace,
        document=jobid,
        outpath=outpath,
    )
    runtime.append(queuemo.recipe.RESULT)
    completed = runtime.next_step()
    assert completed
