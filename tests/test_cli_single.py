# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import pytest
import qvlink
import utilo
import utilotest

import tests


def test_run_single_help(mp, td, capsys):
    cmd = '--help'
    tests.run_single(
        cmd,
        mp,
        td,
        capsys,
    )


def test_run_single_invalid_input(mp, td, capsys):
    cmd = f'-i {__file__}'
    tests.run_single(
        cmd,
        mp,
        td,
        capsys,
        expected=utilo.INVALID_COMMAND,
    )
    assert 'require directory' in utilotest.stderr(capsys)  # pylint:disable=E1101


@utilotest.nightly
def test_run_single(mp, td, capsys):
    # create queuemo todo
    workspace = qvlink.create_todo(hoverpower.DOCU007_PDF, todopath=td.tmpdir)

    # run single queuemo instance in workspace, write output to same workspace
    cmd = f'-i {workspace} -V'
    tests.run_single(
        cmd,
        mp,
        td,
        capsys,
    )

    assert os.path.exists(os.path.join(workspace, 'fastview'))
    assert os.path.exists(os.path.join(workspace, 'result/__optimized__'))


@pytest.mark.skip(reason='supported now, look for other document, enable later')
@utilotest.nightly
def test_no_text_content(td):
    """Stop analysis of `figure only` documents.

    Some pdf printer, print all content to figures, therefore no text is
    detected and avg text size produces errors. We stop analysis before
    running into this error.
    """
    # TODO: LOOK FOR A NEW EXAMPLE
    # create queuemo todo
    workspace = qvlink.create_todo(hoverpower.BACHELOR085_PDF,
                                   todopath=td.tmpdir)
    # run single queuemo instance in workspace, write output to same workspace
    cmd = f'queuemo_single -i {workspace} -V'
    completed = utilo.run(cmd, cwd=td.tmpdir)
    stderr = completed.stderr
    assert '[ERROR] no text in resource' in stderr
    assert 'stop analysis' in stderr


# # @utilotest.nightly
# def test_run_single_different_sink(mp, td):
#     # create queuemo todo
#     workspace = qvlink.create_todo(hoverpower.DOCU007_PDF, todopath=td.tmpdir)

#     sink = td.tmpdir.join( 'different_sink')
#     cmd = f'-i {workspace} -o {sink} -VVV'
#     tests.run_single(
#         cmd,
#         mp,
#         td,
#         capsys=None,
#     )

#     assert os.path.exists(os.path.join(sink, 'fastview'))
#     assert os.path.exists(os.path.join(sink, 'result/__optimized__'))
