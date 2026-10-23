# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import qvlink
import utilotest

import queuemo
import queuemo.recipes
import queuemo.runtime.api
import tests
import tests.conftest
import tests.fixtures.todo
import tests.resources


@tests.conftest.generated
@utilotest.longrun
def test_recipe_validation_success(td, mp):
    """Ensure to create validation result via `pdfinfo` tool"""
    with tests.fixtures.todo.runtime(
            td.tmpdir,
            tests.resources.EXAMPLE_JOB_ID,
            queuemo.recipes.VALIDATION,
            mp,
    ) as rt:  # pylint:disable=C0103
        with utilotest.increased_filecount(td.tmpdir, 'yaml'):
            completed = rt.next_step()
        pdfinfo = qvlink.pdfinfo(tests.resources.EXAMPLE_JOB_ID)
    assert completed
    assert pdfinfo.version.major == 1
    assert pdfinfo.version.minor == 5


@tests.conftest.generated
@utilotest.longrun
def test_recipe_validation_failure(td, mp, capsys):
    """Ensure that validation tool stops with validation error on
    invalid, broken resource"""
    with tests.fixtures.todo.runtime(
            td.tmpdir,
            'broken_resource',
            queuemo.recipes.VALIDATION,
            mp,
    ) as rt:  # pylint:disable=C0103
        with utilotest.increased_filecount(td.tmpdir, 'yaml'):
            completed = rt.next_step()
    assert not completed
    error = utilotest.stderr(capsys)
    assert 'invalid resource' in error, error


@pytest.mark.xfail(reason='software integration')
@tests.conftest.generated
@utilotest.longrun
def test_validation_double_column_flag(td, mp):
    """Inform user about not supported double layout extraction.

    This test will may change later, after double column layout is
    supported.
    """
    # TODO: AUTOMATE DOCUMENTID
    documentid = 'paper006column'  # look in hoverpower if not found
    with tests.fixtures.todo.runtime(
            td.tmpdir,
            document=documentid,
            recipes=queuemo.recipes.VALIDATION,
            config=queuemo.runtime.api.RecipeConfig(skip_unsupported=True),
            mp=mp,
    ) as rt:
        completed = rt.next_step()
        assert not completed, 'exception not raised'
        assert qvlink.notsupported(documentid)
