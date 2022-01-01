# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilatest

import queuemo.recipes.fastview
import tests
import tests.fixtures.todo
import tests.resources


@utilatest.nightly
def test_recipe_fastview_run_single(testdir, monkeypatch):
    completed = run_fastview(
        testdir.tmpdir,
        tests.resources.EXAMPLE_JOB,
        monkeypatch,
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
@utilatest.nightly
def test_recipe_fastview_run_example(jobid, testdir, monkeypatch):
    completed = run_fastview(
        testdir.tmpdir,
        jobid,
        monkeypatch,
    )
    assert completed


def run_fastview(workspace, jobid, monkeypatch):
    with tests.fixtures.todo.runtime(
            workspace,
            jobid,
            recipes=[queuemo.recipes.VALIDATION, queuemo.recipes.FASTVIEW],
            monkeypatch=monkeypatch,
    ) as rt:  # pylint:disable=C0103
        completed = rt.finish()
    return completed
