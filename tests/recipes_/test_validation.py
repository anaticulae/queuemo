# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utilatest

import queuemo
import queuemo.recipes
import queuemo.runtime.api
import tests.fixtures.todo
import tests.resources


@utilatest.longrun
def test_recipe_validation_success(testdir, monkeypatch):
    """Ensure to create validation result via `pdfinfo` tool"""
    with tests.fixtures.todo.runtime(
            testdir.tmpdir,
            tests.resources.EXAMPLE_JOB,
            queuemo.recipes.VALIDATION,
            monkeypatch,
    ) as rt:  # pylint:disable=C0103
        with utilatest.increased_filecount(testdir.tmpdir, 'yaml'):
            completed = rt.next_step()
        pdfinfo = link.pdfinfo(tests.resources.EXAMPLE_JOB)
    assert completed
    assert pdfinfo.version.major == 1
    assert pdfinfo.version.minor == 5


@utilatest.longrun
def test_recipe_validation_failure(testdir, monkeypatch, capsys):
    """Ensure that validation tool stops with validation error on
    invalid, broken resource"""
    with tests.fixtures.todo.runtime(
            testdir.tmpdir,
            'broken_resource',
            queuemo.recipes.VALIDATION,
            monkeypatch,
    ) as rt:  # pylint:disable=C0103
        with utilatest.increased_filecount(testdir.tmpdir, 'yaml'):
            completed = rt.next_step()
    assert not completed
    error = utilatest.stderr(capsys)
    assert 'invalid resource' in error, error


@utilatest.longrun
def test_validation_double_column_flag(testdir, monkeypatch):
    """Inform user about not supported double layout extraction.

    This test will may change later, after double column layout is
    supported.
    """
    # TODO: ATUOMATE DOCUMENTID
    documentid = 'paper006column'  # look in power if not found
    with tests.fixtures.todo.runtime(
            testdir.tmpdir,
            document=documentid,
            recipes=queuemo.recipes.VALIDATION,
            config=queuemo.runtime.api.RecipeConfig(skip_unsupported=True),
            monkeypatch=monkeypatch,
    ) as rt:
        completed = rt.next_step()
        assert not completed, 'exception not raised'
        assert link.notsupported(documentid)
