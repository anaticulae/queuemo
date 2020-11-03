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
import power
import utila
import utilatest

import tests


def test_run_single_help(monkeypatch, testdir, capsys):
    cmd = '--help'
    tests.run_single(
        cmd,
        monkeypatch,
        testdir,
        capsys,
    )


def test_run_single_invalid_input(monkeypatch, testdir, capsys):
    cmd = f'-i {__file__}'
    tests.run_single(
        cmd,
        monkeypatch,
        testdir,
        capsys,
        expected=utila.INVALID_COMMAND,
    )
    assert 'require directory' in utilatest.stderr(capsys)  # pylint:disable=E1101


@utilatest.longrun
def test_run_single(monkeypatch, testdir, capsys):
    # create queuemo todo
    workspace = link.create_todo(power.DOCU07_PDF, todopath=testdir.tmpdir)

    # run single queuemo instance in workspace, write output to same workspace
    cmd = f'-i {workspace} -V'
    tests.run_single(
        cmd,
        monkeypatch,
        testdir,
        capsys,
    )

    assert os.path.exists(os.path.join(workspace, 'fastview'))
    assert os.path.exists(os.path.join(workspace, 'result/__optimized__'))


# # @utilatest.nightly
# def test_run_single_different_sink(monkeypatch, testdir):
#     # create queuemo todo
#     workspace = link.create_todo(power.DOCU07_PDF, todopath=testdir.tmpdir)

#     sink = os.path.join(testdir.tmpdir, 'different_sink')
#     cmd = f'-i {workspace} -o {sink} -VVV'
#     tests.run_single(
#         cmd,
#         monkeypatch,
#         testdir,
#         capsys=None,
#     )

#     assert os.path.exists(os.path.join(sink, 'fastview'))
#     assert os.path.exists(os.path.join(sink, 'result/__optimized__'))
