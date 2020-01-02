# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import configo.directory
import pytest
import utila

import queuemo
import queuemo.cli
import tests


def test_run_main(monkeypatch, testdir, capsys):
    run_queuemo('--version', monkeypatch, testdir, capsys)


def test_run_one_job(monkeypatch, testdir, capsys):
    command = [
        '--%s' % queuemo.cli.RUNTIME,
        '1',  # seconds
        '--%s' % queuemo.cli.WAITING,
        '10',  # mili
        '-VV',
    ]
    run_queuemo(
        command,
        monkeypatch,
        testdir,
        capsys,
    )


@utila.skip_longrun
def test_run_queuemo(testdir):
    command = 'queuemo --runtime=2'
    root = str(testdir)
    todo = os.path.join(root, 'todo')
    ready = os.path.join(root, 'ready')
    tmp = os.path.join(root, 'tmp')
    for item in [todo, ready, tmp]:
        os.makedirs(item)

    # copy to item
    utila.copy_content(tests.TODO, todo, recursive=True)

    env = dict(os.environ)
    env[configo.directory.TODO] = todo
    env[configo.directory.READY] = ready
    env[configo.directory.COMMON] = tmp

    completed = utila.run(command, env=env)
    assert completed.returncode == utila.SUCCESS, str(completed)


def test_queuemo_invalid_parameter(monkeypatch, testdir, capsys):
    command = [
        '--%s' % queuemo.cli.RUNTIME,
        'str',  # invalid input
        '--%s' % queuemo.cli.WAITING,
        'woho',  # invalid input
    ]
    run_queuemo(
        command,
        monkeypatch,
        testdir,
        capsys,
        returncode_=utila.INVALID_COMMAND,
    )


@pytest.mark.parametrize('verbose', [
    ('-V'),
    ('-VV'),
    ('--verbose'),
])
def test_incremental_verbose_flag(verbose, monkeypatch, testdir, capsys):
    run_queuemo(
        [verbose],
        monkeypatch,
        testdir,
        capsys,
    )


def run_queuemo(
        command,
        monkeypatch,
        testdir,
        capsys,
        returncode_=utila.SUCCESS,
):  #pylint: disable=W0613
    if isinstance(command, str):
        command = command.split()

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(sys, 'argv', [queuemo.cli.PROCESS_NAME] + command)

        with pytest.raises(SystemExit) as result:
            queuemo.cli.main()
        assert utila.returncode(result) == returncode_, str(result)
    return capsys
