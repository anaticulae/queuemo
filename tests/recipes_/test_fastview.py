# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilotest

import tests
import tests.fixtures.todo
import tests.resources


@utilotest.nightly
def test_recipe_fastview_run_single(td, mp):
    completed = run_fastview(
        td.tmpdir,
        tests.resources.EXAMPLE_JOB,
        mp,
    )
    assert completed


@pytest.mark.parametrize(
    'jobid',
    [
        '2324123123',
        # 'page_116_images_toc_formular',
        # 'page_72_noimages_toc',
        # 'page_78_images_toc',
        # 'page_83_noimages_toc',
        'master089',
    ])
@utilotest.nightly
def test_recipe_fastview_run_example(jobid, td, mp):
    completed = run_fastview(
        td.tmpdir,
        jobid,
        mp,
    )
    assert completed


def run_fastview(workspace, jobid, mp):
    with tests.fixtures.todo.runtime(
            workspace,
            jobid,
            recipes=[queuemo.recipes.VALIDATION, queuemo.recipes.FASTVIEW],
            mp=mp,
    ) as rt:  # pylint:disable=C0103
        completed = rt.finish()
    return completed
