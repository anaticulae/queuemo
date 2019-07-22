# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir
from os import makedirs
from os.path import exists
from os.path import join

from utila import file_create

from queuemo.utils import copy_content


def test_copy_content_file_to_directory(testdir):
    testdir = str(testdir)
    filename = 'abc.txt'
    file_create(filename)
    destination = join(testdir, 'destination')
    copy_content(filename, destination)

    assert exists(join(destination, filename))


def test_copy_content_file_to_file(testdir):
    testdir = str(testdir)
    filename = 'abc.txt'
    file_create(filename)
    destination = join(testdir, 'cba.txt')
    copy_content(filename, destination)

    assert exists(destination)


def test_copy_content_directory_to_directory(testdir):
    testdir = str(testdir)
    folder = prepare_example(testdir)

    goal = join(testdir, 'goal')
    copy_content(folder, goal)

    assert len(listdir(goal)) == 3, listdir(goal)


def prepare_example(directory):
    folder = join(directory, 'first')

    folder_abc = join(folder, 'abc.txt')
    folder_def = join(folder, 'def.txt')
    folder_ghi = join(folder, 'ghi.txt')

    makedirs(folder)
    for item in [
            folder_abc,
            folder_def,
            folder_ghi,
    ]:
        file_create(item, item)

    return folder
