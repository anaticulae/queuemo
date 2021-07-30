# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import link
import utila

ONE_HOUR = 60 * 60

# TODO: MOVE TO LINK


def remove_outdated():
    for documentid in outdated():
        utila.log(f'complete/fail: {documentid}')
        error = 'not completed in given time'
        link.fail(documentid, error=error)


def outdated():
    todopath = configo.todo(True)
    result = []
    for documentid in os.listdir(todopath):
        info = os.path.join(todopath, documentid, link.JOB_FILE_NAME)
        if utila.file_age(info) < ONE_HOUR:  # pylint:disable=E1101
            continue
        if link.failed(documentid):
            # already failed
            continue
        if link.current(documentid) == link.ProcessState.PUBLISHED:
            continue
        if link.current(documentid) == link.ProcessState.ERROR:
            continue
        result.append(documentid)
    return result
