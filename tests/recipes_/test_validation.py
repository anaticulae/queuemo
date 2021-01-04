# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utilatest

import queuemo
import queuemo.recipes
import tests.fixtures.todo
import tests.resources


def test_recipe_validation(testdir, monkeypatch):  # pylint:disable=W0621
    """Ensure to create validation result via `pdfinfo` tool"""
    with tests.fixtures.todo.runtime(
            testdir.tmpdir,
            tests.resources.EXAMPLE_JOB,
            queuemo.recipes.VALIDATION,
            monkeypatch,
    ) as rt:  # pylint:disable=C0103
        with utilatest.increased_filecount(testdir.tmpdir, 'json'):
            completed = rt.next_step()
        pdfinfo = link.pdfinfo(tests.resources.EXAMPLE_JOB)
    assert completed
    assert os.path.exists(pdfinfo), pdfinfo


def test_recipe_validation_failure(testdir, monkeypatch, capsys):  # pylint:disable=W0621
    """Ensure that validation tool stops with validation error on
    invalid, broken resource"""
    with tests.fixtures.todo.runtime(
            testdir.tmpdir,
            'broken_resource',
            queuemo.recipes.VALIDATION,
            monkeypatch,
    ) as rt:  # pylint:disable=C0103
        with utilatest.increased_filecount(testdir.tmpdir, 'json'):
            completed = rt.next_step()
    assert completed is False
    error = utilatest.stderr(capsys)
    assert 'invalid resource' in error, error
