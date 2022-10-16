# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utilatest

import queuemo.recipes
import tests.conftest
import tests.fixtures.todo
import tests.resources


def run_resultview(workspace, jobid, mp):
    with tests.fixtures.todo.runtime(
            workspace,
            jobid,
            recipes=queuemo.recipes.ORDER,
            mp=mp,
    ) as runner:
        completed = runner.finish()
        # Hint: do not use link, cause multiprocessed tests modify global
        # variables.
        readypath = os.path.join(workspace, 'ready_', jobid)
        # ensure that published worked
        assert os.path.exists(readypath), readypath
    return completed


@utilatest.nightly
def test_recipe_result_run_single(td, mp):  # pylint:disable=W0621
    completed = run_resultview(
        td.tmpdir,
        tests.resources.EXAMPLE_JOB,
        mp,
    )
    assert completed


# pytest.param('8166109011', marks=utilatest.longrun),
# 'page_116_images_toc_formular',
# 'page_38',
# 'page_72_noimages_toc',
# 'page_78_images_toc',
@pytest.mark.parametrize('jobid', [
    pytest.param('2324123123', marks=utilatest.longrun),
    pytest.param('8166109011', marks=utilatest.longrun),
    pytest.param('home025', marks=utilatest.longrun),
    pytest.param('order009', marks=utilatest.longrun),
    pytest.param('master083', marks=utilatest.nightly),
    pytest.param('master089', marks=utilatest.nightly),
])
@tests.conftest.generated
@utilatest.nightly
def test_recipe_result_run_example(jobid, td, mp):
    completed = run_resultview(
        td.tmpdir,
        jobid,
        mp,
    )
    assert completed
