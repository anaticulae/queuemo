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
import utilatest

import queuemo.recipes
import queuemo.runtime.runtime
import tests
import tests.fixtures.todo
import tests.resources


def run_resultview(workspace, jobid, monkeypatch):
    with tests.fixtures.todo.runtime(
            workspace,
            jobid,
            recipes=queuemo.recipes.ORDER,
            monkeypatch=monkeypatch,
    ) as runner:
        completed = runner.finish()
        # Hint: do not use link, cause multiprocessed tests modify global
        # variables.
        readypath = os.path.join(workspace, 'ready_', jobid)
        # ensure that published worked
        assert os.path.exists(readypath), readypath
    return completed


@utilatest.skip_nightly
def test_recipe_result_run_single(testdir, monkeypatch):  # pylint:disable=W0621
    completed = run_resultview(
        testdir.tmpdir,
        tests.resources.EXAMPLE_JOB,
        monkeypatch,
    )
    assert completed


# pytest.param('8166109011', marks=utilatest.skip_longrun),
# 'page_116_images_toc_formular',
# 'page_38',
# 'page_72_noimages_toc',
# 'page_78_images_toc',
@pytest.mark.parametrize('jobid', [
    pytest.param('2324123123', marks=utilatest.skip_longrun),
    pytest.param('8166109011', marks=utilatest.skip_longrun),
    pytest.param('homework25', marks=utilatest.skip_longrun),
    pytest.param('howtowrite_pages9', marks=utilatest.skip_longrun),
    pytest.param('page_83_noimages_toc', marks=utilatest.skip_nightly),
    pytest.param('page_89_noimages_toc', marks=utilatest.skip_nightly),
])
def test_recipe_result_run_example(jobid, testdir, monkeypatch):
    completed = run_resultview(
        testdir.tmpdir,
        jobid,
        monkeypatch,
    )
    assert completed
