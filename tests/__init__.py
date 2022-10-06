#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import contextlib
import os
import shutil
import sys
import threading

import configo.directory
import pytest
import utila

import queuemo
import queuemo.cli.main
import queuemo.cli.single
import tests.__patch__
import tests.resources

LOCK = threading.Lock()


@contextlib.contextmanager
def patch_todo(td, mp, copy=True):  # pylint:disable=W0613
    """Change todo path to avoid overriding test data.

    Args:
        td(fixture): testdir
        mp(fixture): to patch environment variables
        copy(bool): sync data of todo folder
    Yields:
        None: in current working location with setuped environment variables
    """
    with LOCK:
        td = str(td)
        todopath = os.path.join(td, 'todo_')
        readypath = os.path.join(td, 'ready_')
        os.makedirs(readypath, exist_ok=True)
        if copy:
            # Copy content from todo
            # TODO: DO NOT COPY WHOLE DATA TREE
            shutil.copytree(tests.resources.TODO, todopath)
        else:
            os.makedirs(todopath, exist_ok=True)

        with mp.context() as context:
            # Overwrite env vars instead of replacing. If we replace the
            # vars we have to set every single variable again, like
            # accesing rawmaker, sections etc.
            context.setenv(configo.directory.COMMON, td)
            context.setenv(configo.directory.TODO, todopath)
            context.setenv(configo.directory.READY, readypath)
            yield


def run_queuemo(  # pylint:disable=W0613
    cmd,
    mp,
    td,
    capsys,
    process=queuemo.PROCESS,
    runnable=queuemo.cli.main.main,
    expected=utila.SUCCESS,
):
    cmd = cmd.split() if isinstance(cmd, str) else cmd
    with mp.context() as context:
        # Remove all environment vars
        context.setattr(sys, 'argv', [process] + cmd)
        with pytest.raises(SystemExit) as result:
            runnable()
        assert utila.returncode(result) == expected, str(result)
    return capsys


def run_single(
    cmd,
    mp,
    td,
    capsys,
    expected=utila.SUCCESS,
):
    return run_queuemo(
        cmd,
        mp,
        td,
        capsys,
        process='queuemo_single',
        runnable=queuemo.cli.single.main,
        expected=expected,
    )
