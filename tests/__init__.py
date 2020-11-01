#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import contextlib
import os
import shutil
import sys

import pytest
import utila

import queuemo.cli
import tests.resources


@contextlib.contextmanager
def patch_todo(testdir, monkeypatch, copy=True):
    """Change todo path to avoid overriding test data.

    Args:
        testdir(fixture): path where working data is written
        monkeypatch(fixture): to patch environment variables
        copy(bool): sync data of todo folder
    Yields:
        None: in current working location with setuped environment variables
    """
    testdir = str(testdir)
    # TODO: REFACTOR
    from configo.directory import COMMON
    from configo.directory import READY
    from configo.directory import TODO as ENV_TODO

    todopath = os.path.join(testdir, 'todo_')
    readypath = os.path.join(testdir, 'ready_')
    os.makedirs(readypath, exist_ok=True)
    if copy:
        # Copy content from todo
        # TODO: DO NOT COPY WHOLE DATA TREE
        shutil.copytree(tests.resources.TODO, todopath)
    else:
        os.makedirs(todopath, exist_ok=True)

    copy = dict(os.environ)
    with monkeypatch.context() as context:
        # Overwrite env vars instead of replacing. If we replace the vars we
        # have to set every single variable again, like accesing rawmaker,
        # sections etc.
        copy[COMMON] = testdir
        copy[ENV_TODO] = todopath
        copy[READY] = readypath
        context.setattr(os, 'environ', copy)
        yield


def run_queuemo(
        cmd,
        monkeypatch,
        testdir,
        capsys,
        process=queuemo.cli.PROCESS_NAME,
        runnable=queuemo.cli.main,
        expected=utila.SUCCESS,
):
    cmd = cmd.split() if isinstance(cmd, str) else cmd
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(sys, 'argv', [process] + cmd)
        with pytest.raises(SystemExit) as result:
            runnable()
        assert utila.returncode(result) == expected, str(result)
    return capsys


