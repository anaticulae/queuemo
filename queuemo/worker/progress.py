# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import configo
import utila

PROGRESS_FILENAME = 'inprogress'


def update(jobid: int, progress: int):
    assert 0 <= progress <= 100, f'progress is out of range: {progress}'
    path = progress_file(jobid)
    assert os.path.exists(path), path
    progress = str(progress).zfill(3)
    utila.file_replace(path, progress)


def start(jobid: int):
    # TODO: Remove, replace with link
    path = progress_file(jobid)
    assert not os.path.exists(path), path

    # Mark folder as in progress and start with 0 percent
    utila.file_create(path, '000')


def inprogress(jobid: int) -> bool:
    # TODO: Remove, replace with link
    path = progress_file(jobid)
    return os.path.exists(path)


def progress_file(jobid: int) -> str:
    todopath = configo.todo(True)
    result = os.path.join(todopath, jobid, PROGRESS_FILENAME)
    return result
