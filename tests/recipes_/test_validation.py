# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import pytest
import utilatest

import queuemo
import queuemo.recipes
import queuemo.runtime.api
import tests
import tests.conftest
import tests.fixtures.todo
import tests.resources


@tests.conftest.generated
@utilatest.longrun
def test_recipe_validation_success(td, mp):
    """Ensure to create validation result via `pdfinfo` tool"""
    with tests.fixtures.todo.runtime(
            td.tmpdir,
            tests.resources.EXAMPLE_JOB,
            queuemo.recipes.VALIDATION,
            mp,
    ) as rt:  # pylint:disable=C0103
        with utilatest.increased_filecount(td.tmpdir, 'yaml'):
            completed = rt.next_step()
        pdfinfo = link.pdfinfo(tests.resources.EXAMPLE_JOB)
    assert completed
    assert pdfinfo.version.major == 1
    assert pdfinfo.version.minor == 5


@tests.conftest.generated
@utilatest.longrun
def test_recipe_validation_failure(td, mp, capsys):
    """Ensure that validation tool stops with validation error on
    invalid, broken resource"""
    with tests.fixtures.todo.runtime(
            td.tmpdir,
            'broken_resource',
            queuemo.recipes.VALIDATION,
            mp,
    ) as rt:  # pylint:disable=C0103
        with utilatest.increased_filecount(td.tmpdir, 'yaml'):
            completed = rt.next_step()
    assert not completed
    error = utilatest.stderr(capsys)
    assert 'invalid resource' in error, error


@pytest.mark.xfail(reason='software integration')
@tests.conftest.generated
@utilatest.longrun
def test_validation_double_column_flag(td, mp):
    """Inform user about not supported double layout extraction.

    This test will may change later, after double column layout is
    supported.
    """
    # TODO: AUTOMATE DOCUMENTID
    documentid = 'paper006column'  # look in power if not found
    with tests.fixtures.todo.runtime(
            td.tmpdir,
            document=documentid,
            recipes=queuemo.recipes.VALIDATION,
            config=queuemo.runtime.api.RecipeConfig(skip_unsupported=True),
            mp=mp,
    ) as rt:
        completed = rt.next_step()
        assert not completed, 'exception not raised'
        assert link.notsupported(documentid)
