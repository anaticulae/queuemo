# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import queuemo.recipes
import tests.fixtures.todo
import tests.resources


@utilatest.nightly
def test_chapter(td, mp, capsys):
    """Ensure that --docinfo {pagecount} is passed to chapter decider."""
    validation = queuemo.recipes.VALIDATION.copy()
    plan = queuemo.recipes.RESULT.copy()
    # magic is required to generate words which is required by chapter
    plan.shrink('before magic chapter'.split())
    with tests.fixtures.todo.runtime(
            workspace=td.tmpdir,
            document=tests.resources.EXAMPLE_JOB,
            recipes=(validation, plan),
            mp=mp,
    ) as rt:  # pylint:disable=C0103
        assert rt.next_step()
        assert rt.next_step()
    expected = '--docinfo 9english'
    stdout = utilatest.stdout(capsys)
    assert expected in stdout
