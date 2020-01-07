# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import pytest
import utila

import queuemo
import queuemo.recipes.runner
import tests.resources


@pytest.fixture
def example_8166(testdir):
    root = str(testdir)
    source = os.path.join(
        tests.resources.TODO,
        tests.resources.EXAMPLE_JOB,
        tests.resources.EXAMPLE_JOB,
    )
    destination = os.path.join(
        root,
        tests.resources.EXAMPLE_JOB,
    )
    utila.file_copy(source, destination)
    return root


def copy_todo(jobid: str, destination: str):
    source = os.path.join(tests.resources.TODO, jobid, jobid)
    destination = os.path.join(destination, jobid)
    utila.file_copy(source, destination)


@contextlib.contextmanager
def runtime(
        workspace,
        document,
        recipes,
        monkeypatch,
) -> queuemo.recipes.runner.RecipeRuntime:
    workspace = str(workspace)
    todopath = os.path.join(workspace, '_todo')
    outpath = os.path.join(workspace, 'outpath')
    if not isinstance(recipes, list):
        recipes = [recipes]

    with tests.patch_todo(todopath, monkeypatch, copy=False):
        current = queuemo.recipes.runner.RecipeRuntime(
            workspace=workspace,
            document=document,
            outpath=outpath,
        )
        for item in recipes:
            current.append(item)
        yield current
