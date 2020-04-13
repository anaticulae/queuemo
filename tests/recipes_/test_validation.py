# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila

import queuemo
import queuemo.recipes
import tests
import tests.fixtures.todo


def test_recipe_validation(testdir, monkeypatch):  # pylint:disable=W0621
    """Ensure to create validation result via `pdfinfo` tool"""
    workspace = str(testdir)
    with tests.fixtures.todo.runtime(
            workspace,
            tests.resources.EXAMPLE_JOB,
            queuemo.recipes.VALIDATION,
            monkeypatch,
    ) as rt:  # pylint:disable=C0103
        with utila.increased_filecount(workspace, 'json'):
            completed = rt.next_step()
        pdfinfo = link.pdfinfo(tests.resources.EXAMPLE_JOB)
    assert completed
    assert os.path.exists(pdfinfo), pdfinfo


def test_recipe_validation_failure(testdir, monkeypatch, capsys):  # pylint:disable=W0621
    """Ensure that validation tool stops with validation error on
    invalid, broken resource"""
    workspace = str(testdir)
    with tests.fixtures.todo.runtime(
            workspace,
            'broken_resource',
            queuemo.recipes.VALIDATION,
            monkeypatch,
    ) as rt:  # pylint:disable=C0103
        with utila.increased_filecount(workspace, 'json'):
            completed = rt.next_step()
    assert completed is False
    log = capsys.readouterr().out
    assert 'invalid resource' in log, log
