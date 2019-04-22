# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

from pytest import raises
from utila.test import run
from utila.test import skip_not_virtual

from queuemo import ROOT
from queuemo.command import main


@skip_not_virtual
def test_run_queuemo():
    """Install queuemo and run queuemo --help to ensure basic function"""
    uninstall = 'pip uninstall queuemo -y'
    install = 'python setup.py install && queuemo --help'

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)
    assert completed.returncode == 0, str(completed)


def test_run_main(monkeypatch):
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(sys, 'argv', ['-v'])

        with raises(SystemExit) as result:
            main()
        result = str(result)
        assert 'SystemExit: 0' in result, result
