# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

from pytest import mark
from pytest import raises
from utila import SUCCESS
from utila.test import run
from utila.test import skip_not_virtual

from queuemo import ROOT
from queuemo.command import PROCESS_NAME
from queuemo.command import RUNTIME
from queuemo.command import WAITING
from queuemo.command import main


@skip_not_virtual
def test_run_queuemo():
    """Install queuemo and run queuemo --help to ensure basic function"""
    uninstall = 'pip uninstall queuemo -y'
    install = 'python setup.py install && queuemo --help'

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)  # run setup.py
    assert completed.returncode == SUCCESS, str(completed)


def test_run_main(monkeypatch):
    run_queuemo('--version', monkeypatch, None)


@mark.skip
def test_run_one_job(monkeypatch):
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
        None,
    )


@mark.skip
@mark.parametrize('verbose', [
    ('-V'),
    ('-VV'),
    ('--verbose'),
])
def test_incremental_verbose_flag(verbose, monkeypatch):
    run_queuemo(
        [verbose],
        monkeypatch,
        None,
    )


def run_queuemo(command, monkeypatch, testdir):  #pylint: disable=W0613
    if isinstance(command, str):
        command = command.split()

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(sys, 'argv', [PROCESS_NAME] + command)

        with raises(SystemExit) as result:
            main()
        result = str(result)
        assert 'SystemExit: 0' in result, result
