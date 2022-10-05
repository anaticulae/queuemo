# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo.directory
import pytest
import utila
import utilatest

import queuemo
import queuemo.cli.main
import tests
import tests.resources


def test_run_main(mp, td, capsys):
    tests.run_queuemo('--version', mp, td, capsys)


@pytest.mark.timeout(10, method="thread")  # common todo contains some data
def test_run_one_job(mp, td, capsys):
    # TODO: PATCH ENV VARS
    command = [
        '--%s' % queuemo.cli.main.RUNTIME,
        '1',  # seconds
        '--%s' % queuemo.cli.main.WAITING,
        '10',  # mili
        '-VV',
    ]
    tests.run_queuemo(
        command,
        mp,
        td,
        capsys,
    )


@utilatest.nightly
def test_run_queuemo(td):
    command = 'queuemo --runtime=2'
    root = str(td)
    todo = os.path.join(root, 'todo')
    ready = os.path.join(root, 'ready')
    tmp = os.path.join(root, 'tmp')
    for item in [todo, ready, tmp]:
        os.makedirs(item)

    # copy to item
    utila.copy_content(tests.resources.TODO, todo, recursive=True)

    env = dict(os.environ)
    env[configo.directory.TODO] = todo
    env[configo.directory.READY] = ready
    env[configo.directory.COMMON] = tmp

    completed = utila.run(command, env=env)
    assert completed.returncode == utila.SUCCESS, str(completed)


def test_queuemo_invalid_parameter(mp, td, capsys):
    command = [
        '--%s' % queuemo.cli.main.RUNTIME,
        'str',  # invalid input
        '--%s' % queuemo.cli.main.WAITING,
        'woho',  # invalid input
    ]
    tests.run_queuemo(
        command,
        mp,
        td,
        capsys,
        expected=utila.INVALID_COMMAND,
    )


@pytest.mark.parametrize('verbose', [
    ('-V'),
    ('-VV'),
    ('--verbose'),
])
def test_incremental_verbose_flag(verbose, mp, td, capsys):
    cmd = f'{verbose} --runtime 0'
    tests.run_queuemo(cmd, mp, td, capsys)
