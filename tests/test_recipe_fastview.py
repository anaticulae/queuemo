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

import queuemo.recipes.fastview
import tests
import tests.resources
from tests.fixtures.todo import copy_todo
from tests.fixtures.todo import example_8166  # pylint:disable=W0611


@utila.skip_longrun
def test_recipe_fastview_extract_resources(example_8166):  # pylint:disable=W0621
    """Ensure that resources for title page analysation is created."""
    workspace = str(example_8166)
    with tests.increased_filecount(workspace, 'yaml'):
        queuemo.recipes.fastview.extract_resource(
            workspace,
            tests.resources.EXAMPLE_JOB,
        )


@utila.skip_longrun
def test_recipe_fastview_titlepage(example_8166):  # pylint:disable=W0621
    workspace = str(example_8166)
    queuemo.recipes.fastview.extract_resource(
        workspace,
        tests.resources.EXAMPLE_JOB,
    )
    with tests.increased_filecount(workspace, 'yaml'):
        queuemo.recipes.fastview.titlepage(
            workspace,
            tests.resources.EXAMPLE_JOB,
        )


@utila.skip_longrun
def test_recipe_fastview_publish(example_8166, monkeypatch):  # pylint:disable=W0621
    workspace = str(example_8166)
    queuemo.recipes.fastview.extract_resource(
        workspace,
        tests.resources.EXAMPLE_JOB,
    )
    queuemo.recipes.fastview.titlepage(
        workspace,
        tests.resources.EXAMPLE_JOB,
    )

    todopath = os.path.join(workspace, '_todo')
    with tests.patch_todo(todopath, monkeypatch):
        with tests.increased_filecount(todopath, 'yaml'):
            # ensure to copy **user result files**
            queuemo.recipes.fastview.publish(
                workspace,
                tests.resources.EXAMPLE_JOB,
            )


@utila.skip_longrun
def test_recipe_fastview_run(example_8166, monkeypatch):  # pylint:disable=W0621
    workspace = str(example_8166)

    todopath = os.path.join(workspace, '_todo')
    with tests.patch_todo(todopath, monkeypatch):
        queuemo.recipes.fastview.run(workspace, tests.resources.EXAMPLE_JOB)


@utila.skip_longrun
@pytest.mark.parametrize('jobid', [
    '2324123123',
    'page_116_images_toc_formular',
    'page_72_noimages_toc',
    'page_78_images_toc',
    'page_83_noimages_toc',
    pytest.param(
        'page_89_noimages_toc',
        marks=pytest.mark.xfail(reason='problem in groupe module'),
    ),
])
def test_recipe_fastview_run_example(jobid, testdir, monkeypatch):  # pylint:disable=W0621
    workspace = str(testdir)
    copy_todo(jobid, workspace)

    todopath = os.path.join(workspace, '_todo')
    with tests.patch_todo(todopath, monkeypatch):
        queuemo.recipes.resultview.run(workspace, jobid)
