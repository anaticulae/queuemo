# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos.directory
import pytest
import utilo
import utilotest

import queuemo
import queuemo.cli.main
import tests
import tests.resources


def test_run_main(mp, td, capsys):
    tests.run_queuemo('--version', mp, td, capsys)


@pytest.mark.timeout(10, method="thread")  # common todo contains some data
def test_run_one_job(mp, td, capsys):
    # TODO: PATCH ENV VARS
    cmd = [
        f'--{queuemo.cli.main.RUNTIME}',
        '1',  # seconds
        f'--{queuemo.cli.main.WAITING}',
        '10',  # mili
        '-VV',
    ]
    tests.run_queuemo(
        cmd,
        mp,
        td,
        capsys,
    )


@utilotest.nightly
def test_run_queuemo(td):
    cmd = 'queuemo --runtime=2'
    todo = td.tmpdir.join('todo')
    ready = td.tmpdir.join('ready')
    tmp = td.tmpdir.join('tmp')
    for item in (todo, ready, tmp):
        os.makedirs(item)
    # copy to item
    utilo.copy_content(
        tests.resources.TODO,
        todo,
        recursive=True,
        unlock=True,
    )
    env = dict(os.environ)
    env[configos.directory.TODO] = str(todo)
    env[configos.directory.READY] = str(ready)
    env[configos.directory.COMMON] = str(tmp)
    completed = utilo.run(cmd, env=env)
    assert completed.returncode == utilo.SUCCESS, str(completed)


def test_queuemo_invalid_parameter(mp, td, capsys):
    cmd = [
        f'--{queuemo.cli.main.RUNTIME}',
        'str',  # invalid input
        f'--{queuemo.cli.main.WAITING}',
        'woho',  # invalid input
    ]
    tests.run_queuemo(
        cmd,
        mp,
        td,
        capsys,
        expected=utilo.INVALID_COMMAND,
    )


@pytest.mark.parametrize('verbose', [
    ('-V'),
    ('-VV'),
    ('--verbose'),
])
def test_incremental_verbose_flag(verbose, mp, td, capsys):
    cmd = f'{verbose} --runtime 0'
    tests.run_queuemo(cmd, mp, td, capsys)
