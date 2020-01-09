#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import contextlib
import glob
import os
import shutil

import utila

import tests.resources


@contextlib.contextmanager
def patch_todo(testdir, monkeypatch, copy=True):
    """Change todo path to avoid overriding test data.

    Args:
        testdir: path where working data is written
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


@contextlib.contextmanager
def increased_filecount(path: str, ending: str = None):
    """Ensure to create some files while running operations in yieldet
    state."""
    # TODO: MOVE TO UTILA TEST
    assert os.path.exists(path), str(path)
    pattern = '**/*.*' if ending is None else f'**/*.{ending}'
    with utila.chdir(path):
        before = list(glob.glob(pattern, recursive=True))
        yield
        after = list(glob.glob(pattern, recursive=True))
    assert len(after) > len(before), f'{before}\n\n{after}'
