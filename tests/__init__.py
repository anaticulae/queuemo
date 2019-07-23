#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from contextlib import contextmanager
from os import makedirs
from os.path import exists
from os.path import join
from shutil import copytree

from queuemo import ROOT

TEST_DATA = join(ROOT, 'tests/resources')
assert exists(TEST_DATA), TEST_DATA

TODO = join(TEST_DATA, 'todo')
assert exists(TODO), TODO

EXAMPLE_JOB = '8166109011'

EXAMPLE_JOB_PATH = join(TODO, EXAMPLE_JOB)
assert exists(EXAMPLE_JOB_PATH), EXAMPLE_JOB_PATH

EXAMPLE_PDF = join(EXAMPLE_JOB_PATH, EXAMPLE_JOB)
assert exists(EXAMPLE_PDF), str(EXAMPLE_PDF)


@contextmanager
def patch_todo(testdir, monkeypatch):
    testdir = str(testdir)
    import os
    from configo.share import COMMON
    from configo.share import READY
    from configo.share import TODO as ENV_TODO

    makedirs(join(testdir, 'ready'))
    # Copy content from todo
    copytree(TODO, join(testdir, 'todo'))
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(
            os, 'environ', {
                COMMON: testdir,
                ENV_TODO: join(testdir, 'todo'),
                READY: join(testdir, 'ready'),
            })
        yield
