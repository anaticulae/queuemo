# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys
from os import makedirs
from os.path import join

from configo.share import READY
from configo.share import TODO
from pytest import mark
from pytest import raises
from utila import INVALID_COMMAND
from utila import SUCCESS
from utila import copy_content
from utila import returncode
from utila import skip_longrun
from utila.test import run
from utila.test import skip_nonvirtual

from queuemo import ROOT
from queuemo.command import PROCESS_NAME
from queuemo.command import RUNTIME
from queuemo.command import WAITING
from queuemo.command import main
from queuemo.utils import run as run_replace_me
from tests import TODO as TODO_SOURCE


@skip_nonvirtual
def test_install_and_run_queuemo():
    """Install queuemo and run queuemo --help to ensure basic function"""
    uninstall = 'pip uninstall queuemo -y'
    install = 'python setup.py install && queuemo --help'

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)  # run setup.py
    assert completed.returncode == SUCCESS, str(completed)


def test_run_main(monkeypatch, testdir, capsys):
    run_queuemo('--version', monkeypatch, testdir, capsys)


def test_run_one_job(monkeypatch, testdir, capsys):
    command = [
        '--%s' % RUNTIME,
        '1',  # seconds
        '--%s' % WAITING,
        '10',  # mili
        '-VV',
    ]
    run_queuemo(
        command,
        monkeypatch,
        testdir,
        capsys,
    )


@skip_longrun
def test_run_queuemo(testdir):
    command = 'queuemo --runtime=2'
    root = str(testdir)
    todo = join(root, 'todo')
    ready = join(root, 'ready')
    tmp = join(root, 'tmp')
    for item in [todo, ready, tmp]:
        makedirs(item)

    # copy to item
    copy_content(TODO_SOURCE, todo, recursive=True)

    env = dict(os.environ)
    env[TODO] = todo
    env[READY] = ready
    env['SHARED_TMP'] = tmp  # TODO: REPLACE WITH CONFIGO

    # TODO: REPLACE AFTER UPGRADING UTILA
    completed = run_replace_me(command, env=env)
    assert completed.returncode == SUCCESS, str(completed)


def test_queuemo_invalid_parameter(monkeypatch, testdir, capsys):
    command = [
        '--%s' % RUNTIME,
        'str',  # invalid input
        '--%s' % WAITING,
        'woho',  # invalid input
    ]
    run_queuemo(
        command,
        monkeypatch,
        testdir,
        capsys,
        returncode_=INVALID_COMMAND,
    )


@mark.parametrize('verbose', [
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


def run_queuemo(command, monkeypatch, testdir, capsys, returncode_=SUCCESS):  #pylint: disable=W0613
    if isinstance(command, str):
        command = command.split()

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(sys, 'argv', [PROCESS_NAME] + command)

        with raises(SystemExit) as result:
            main()
        assert returncode(result) == returncode_, str(result)
    return capsys
