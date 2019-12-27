#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import contextlib
import glob
import os
import shutil

import utila

import queuemo

TEST_DATA = os.path.join(queuemo.ROOT, 'tests/resources')
assert os.path.exists(TEST_DATA), TEST_DATA

TODO = os.path.join(TEST_DATA, 'todo')
assert os.path.exists(TODO), TODO

EXAMPLE_JOB = '8166109011'

EXAMPLE_JOB_PATH = os.path.join(TODO, EXAMPLE_JOB)
assert os.path.exists(EXAMPLE_JOB_PATH), EXAMPLE_JOB_PATH

EXAMPLE_PDF = os.path.join(EXAMPLE_JOB_PATH, EXAMPLE_JOB)
assert os.path.exists(EXAMPLE_PDF), str(EXAMPLE_PDF)


@contextlib.contextmanager
def patch_todo(testdir, monkeypatch):
    testdir = str(testdir)
    from configo.directory import COMMON
    from configo.directory import READY
    from configo.directory import TODO as ENV_TODO

    os.makedirs(os.path.join(testdir, 'ready'))
    # Copy content from todo
    shutil.copytree(TODO, os.path.join(testdir, 'todo'))

    copy = dict(os.environ)
    with monkeypatch.context() as context:
        # Overwrite env vars instead of replacing. If we replace the vars we
        # have to set every single variable again, like accesing rawmaker,
        # sections etc.
        copy[COMMON] = testdir
        copy[ENV_TODO] = os.path.join(testdir, 'todo')
        copy[READY] = os.path.join(testdir, 'ready')
        context.setattr(os, 'environ', copy)
        yield


@contextlib.contextmanager
def increased_filecount(path: str):
    """Ensure to create some files while running operations in yieldet
    state."""
    # TODO: MOVE TO UTILA TEST
    assert os.path.exists(path), str(path)
    with utila.chdir(path):
        before = list(glob.glob('**', recursive=True))
        yield
        after = list(glob.glob('**', recursive=True))
    assert after > before
